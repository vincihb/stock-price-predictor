from api.alpha_vantage.AlphaVantageAPI import AlphaVantageAPI
from api.alpha_vantage.HAVCache import HAVCache
import datetime as dt
import json
import time


class HistoricAlphaVantageAPI(AlphaVantageAPI):
    DAILY_URL = AlphaVantageAPI.DAILY_URL.replace('__OUTPUT_SIZE__', 'full')

    def __init__(self):
        AlphaVantageAPI.__init__(self)
        self._cache = HAVCache()

    # User needs to input a datetime date class that is converted to a unique ordinal number
    def get_symbol_on_date(self, symbol, date):
        print("Getting symbol %s" % (symbol,))
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

            self.store_data(symbol, date, result)
            self.store_meta_data(symbol)
            exit()
        return result

    # Stores the actual data we receive from Alpha Vantage into the cache
    def store_data(self, symbol, date, result):
        daily_time_series = result['Time Series (Daily)']
        for key in daily_time_series:
            a = ()
            for item in daily_time_series[key]:
                a = a + (daily_time_series[key][item],)
            date_string = key
            year_time_series = int(date_string[0:4])
            month_time_series = int(date_string[5:7])
            day_time_series = int(date_string[8:10])
            self._cache.store_result_data(symbol, dt.date(year_time_series,
                                                          month_time_series, day_time_series).toordinal(), a)

    def store_meta_data(self, symbol):
        return self._cache.store_result_meta_data(symbol, dt.date.today().toordinal())

    # Checks cache for symbol on specific date
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
