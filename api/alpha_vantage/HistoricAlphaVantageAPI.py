from api.alpha_vantage.AlphaVantageAPI import AlphaVantageAPI
from api.alpha_vantage.HAVCache import HAVCache
import datetime
import json
import time


class HistoricAlphaVantageAPI(AlphaVantageAPI):
    DAILY_URL = AlphaVantageAPI.DAILY_URL.replace('__OUTPUT_SIZE__', 'full')

    def __init__(self):
        AlphaVantageAPI.__init__(self)
        self._cache = HAVCache()

    def get_symbol_on_date(self, symbol, date):
        self.symbol_request_on_date(self.DAILY_URL, symbol, date)

    def symbol_request_on_date(self, url, symbol, date, retries=0):
        api_url = url.replace('__SYMBOL__', symbol)
        result = self.try_cache(symbol, date)
        if result is None:
            result = json.loads(self.make_request(api_url))

            if result == 'Error' or 'Meta Data' not in result:
                if 'Error Message' in result:
                    print('Error retrieving data from HAV for %s' % (symbol,))
                    self._cache.store_result_data(symbol, date, 'NOT_FOUND')
                    return AlphaVantageAPI.NOT_FOUND_RESPONSE

                if retries < 5:
                    print('HAV_API: Retrying for symbol %s, have retried %d/5 times...' % (symbol, retries))
                    time.sleep(20)
                    return self.symbol_request_on_date(url, symbol, retries + 1)
                else:
                    print('HAV_API Timeout: Unable to get data for %s within retry limit' % (symbol,))
                    return None

            # Figure out how to put the json file's output into the database
            # Loop through the entries, enter them into the database, and stop once you are past
            # the date retrieved
            # save what we get to the cache if it's valid
            self._cache.store_result_data(symbol, date, json.dumps(result))
            self._cache.store_result_meta_data(symbol, datetime.date.today().day)

        return result

    def try_cache(self, symbol, date):
        result = self._cache.check_cache(symbol, date)
        if result is not None:
            print('Found data in cache!')
            result = result['payload']
            if result == 'NOT_FOUND':
                return AlphaVantageAPI.NOT_FOUND_RESPONSE
            else:
                return json.loads(result)

        return None
