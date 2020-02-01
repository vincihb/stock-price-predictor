import json
import time
import requests as req
from os import path

from api.alpha_vantage.AVCache import AVCache

"""
Class for calling the AlphaVantage API to retrieve stock data
Be wary that AlphaVantage is the most restrictive API we use and has strict restrictions on usage
    Currently they support at maximum 5 requests per minute and 500 requests a day -- we should consider replacing this
    with a more robust and accessible API if possible
"""

'''TODO: AV cache to prevent need for going back to the AV server unless expressly needed'''

'''consider retry loop'''


class AlphaVantageAPI:
    BASE_URL = 'https://www.alphavantage.co/query?'
    QUOTE_URL = BASE_URL + 'function=GLOBAL_QUOTE&apikey=__API_KEY__&symbol=__SYMBOL__'
    WEEKLY_URL = BASE_URL + 'function=TIME_SERIES_WEEKLY&apikey=__API_KEY__&symbol=__SYMBOL__'
    DAILY_URL = BASE_URL + 'function=TIME_SERIES_DAILY&apikey=__API_KEY__&symbol=__SYMBOL__'
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

    def __init__(self):
        self._local_dir = path.dirname(path.abspath(__file__))
        self._config_path = path.join(self._local_dir, '..', '..', 'config', 'stock_api.json')
        with open(self._config_path) as json_data:
            d = json.load(json_data)

        self.API_KEY = d['API_KEY']
        self._cache = AVCache()

    def get_intraday_data(self, symbol, interval='60min', output_size='compact'):
        prepared_url = AlphaVantageAPI.INTRADAY_URL \
            .replace('__INTERVAL__', interval) \
            .replace('__OUTPUT_SIZE__', output_size)

        return self.symbol_request(prepared_url, symbol)

    def get_quote(self, symbol):
        quote = "QUOTE"
        result = self._cache.check_cache(symbol, quote)
        if result is not None:
            print('Found data in cache!')
            return json.loads(result['payload'])
        else:
            result = self.symbol_request(AlphaVantageAPI.QUOTE_URL, symbol)['Global Quote']
            self._cache.store_result(symbol, quote, json.dumps(result))
            return result

    def get_weekly_data(self, symbol):
        week = 'WEEK'
        result = self._cache.check_cache(symbol, week)
        if result is not None:
            print('Found data in cache!')
            return json.loads(result['payload'])
        else:
            result = self.symbol_request(AlphaVantageAPI.WEEKLY_URL, symbol)
            self._cache.store_result(symbol, week, json.dumps(result))
            return result

    def get_daily_data(self, symbol):
        day = 'DAY'
        result = self._cache.check_cache(symbol, day)
        if result is not None:
            print('Found data in cache!')
            return json.loads(result['payload'])
        else:
            result = self.symbol_request(AlphaVantageAPI.DAILY_URL, symbol)
            self._cache.store_result(symbol, day, json.dumps(result))
            return result

    def symbol_request(self, url, symbol, retries=0):
        api_url = url.replace('__SYMBOL__', symbol)
        result = json.loads(self.make_request(api_url))
        if 'Global Quote' not in result and 'Meta Data' not in result:
            if retries < 5:
                print('AV_API: Retrying for symbol %s, have retried %d/5 times...' % (symbol, retries))
                time.sleep(5)
                return self.symbol_request(url, symbol, retries + 1)
            else:
                print('AV_API Timeout: Unable to get data for %s within retry limit' % (symbol,))
                return None

        return result

    def make_request(self, url):
        final_url = url.replace('__API_KEY__', self.API_KEY)
        print("AV_API: Request OUT to: %s" % (final_url,))
        result = req.get(final_url)
        if result.status_code == req.codes.ok:
            return result.text
        else:
            return 'Error'


a = AlphaVantageAPI()
print(a.get_daily_data('TSLA'))
