import json
import time
import requests as req
from os import path

from api.alpha_vantage.AVCache import AVCache
from api.meta.APIUsageTracker import APIUsageTracker

"""
Class for calling the AlphaVantage API to retrieve stock data
Be wary that AlphaVantage is the most restrictive API we use and has strict restrictions on usage
    Currently they support at maximum 5 requests per minute and 500 requests a day -- we should consider replacing this
    with a more robust and accessible API if possible
"""


class AlphaVantageAPI:
    API_CALL_LIMIT = 500
    BASE_URL = 'https://www.alphavantage.co/query?'
    QUOTE_URL = BASE_URL + 'function=GLOBAL_QUOTE&apikey=__API_KEY__&symbol=__SYMBOL__'
    WEEKLY_URL = BASE_URL + 'function=TIME_SERIES_WEEKLY&apikey=__API_KEY__&symbol=__SYMBOL__'
    DAILY_URL = BASE_URL + 'function=TIME_SERIES_DAILY&symbol=__SYMBOL__&' + \
                'outputsize=__OUTPUT_SIZE__&apikey=__API_KEY__'
    INTRADAY_URL = BASE_URL + 'function=TIME_SERIES_INTRADAY&symbol=__SYMBOL__&interval=__INTERVAL__&' + \
                   'outputsize=__OUTPUT_SIZE__&apikey=__API_KEY__'

    INTERVALS = {
        'MINUTE': '1min',
        '5_MIN': '5min',
        '15_MIN': '15min',
        'HALF_HOUR': '30min',
        'HOUR': '60min'
    }

    OUTPUT_SIZE = {
        'COMPACT': 'compact',
        'FULL': 'full'
    }

    NOT_FOUND_RESPONSE = {
        "Global Quote": {
            "01. symbol": "Not Found",
            "02. open": "Not Found",
            "03. high": "Not Found",
            "04. low": "Not Found",
            "05. price": "Not Found",
            "06. volume": "Not Found",
            "07. latest trading day": "Not Found",
            "08. previous close": "Not Found",
            "09. change": "Not Found",
            "10. change percent": "Not Found"
        },
        "Message": "Note that this ticker was not found"
    }

    def __init__(self):
        self._local_dir = path.dirname(path.abspath(__file__))
        self._config_path = path.join(self._local_dir, '..', '..', 'config', 'stock_api.json')
        with open(self._config_path) as json_data:
            d = json.load(json_data)

        self.API_KEY = d['API_KEY']
        self.usage = self._get_usages()
        self._cache = AVCache()
        self._last_req_type = None

    def get_remaining_api_calls(self):
        remaining = AlphaVantageAPI.API_CALL_LIMIT - self.usage
        print('You have used %d/%d requests' % (self.usage, AlphaVantageAPI.API_CALL_LIMIT))
        print('Leaving %d requests for today' % remaining)
        return remaining

    def get_intraday_data(self, symbol, interval='60min', output_size='compact'):
        self._last_req_type = 'INTRA'
        prepared_url = AlphaVantageAPI.INTRADAY_URL \
            .replace('__INTERVAL__', interval) \
            .replace('__OUTPUT_SIZE__', output_size)

        return self.symbol_request(prepared_url, symbol)

    def get_quote(self, symbol, force_reload=False):
        self._last_req_type = 'QUOTE'
        return self.symbol_request(AlphaVantageAPI.QUOTE_URL, symbol, force_reload=force_reload)

    def get_parsed_quote(self, symbol, force_reload=False):
        return self.get_quote(symbol, force_reload)['Global Quote']

    def get_weekly_data(self, symbol):
        self._last_req_type = 'WEEK'
        return self.symbol_request(AlphaVantageAPI.WEEKLY_URL, symbol)

    def get_daily_data(self, symbol):
        self._last_req_type = 'DAY'
        return self.symbol_request(AlphaVantageAPI.DAILY_URL, symbol)

    def symbol_request(self, url, symbol, retries=0, force_reload=False):
        api_url = url.replace('__SYMBOL__', symbol)
        result = self.try_cache(symbol, force_reload=force_reload)
        if result is None or force_reload is True:
            result = json.loads(self.make_request(api_url))

            if result == 'Error' or 'Global Quote' not in result and 'Meta Data' not in result:
                if 'Error Message' in result:
                    print('Error retrieving data from AV for %s' % (symbol,))
                    self._cache.store_result(symbol, self._last_req_type, 'NOT_FOUND')
                    return AlphaVantageAPI.NOT_FOUND_RESPONSE

                if retries < 5:
                    print('AV_API: Retrying for symbol %s, have retried %d/5 times...' % (symbol, retries))
                    time.sleep(20)
                    return self.symbol_request(url, symbol, retries + 1)
                else:
                    print('AV_API Timeout: Unable to get data for %s within retry limit' % (symbol,))
                    return None

            # save what we get to the cache if it's valid
            self._cache.store_result(symbol, self._last_req_type, json.dumps(result))

        return result

    def try_cache(self, symbol, force_reload=False):
        result = self._cache.check_cache(symbol, self._last_req_type, force_reload=force_reload)
        if result is not None:
            print('Found data in cache!')
            result = result['payload']
            if result == 'NOT_FOUND':
                return AlphaVantageAPI.NOT_FOUND_RESPONSE
            else:
                return json.loads(result)

        return None

    def make_request(self, url):
        if self.usage >= 500:
            print('API CALL LIMIT EXCEEDED -- failing out')
            return 'Error'

        final_url = url.replace('__API_KEY__', self.API_KEY)
        print("AV_API: Request OUT to: %s" % (final_url,))
        result = req.get(final_url)
        time.sleep(5)
        if result.status_code == req.codes.ok:
            # if we get a valid response, bump the usages for the api key
            self.usage += 1
            APIUsageTracker().update_use_count(self.API_KEY, self.usage)
            return result.text
        else:
            return 'Error'

    def _get_usages(self):
        count = APIUsageTracker().get_use_count(self.API_KEY)
        if count is None:
            return 0
        else:
            return count
