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
    def get_symbol_on_date(self, symbol, date, force_reload=False):
        print("Getting symbol %s" % (symbol,))
        if isinstance(date, dt.date):
            date = date.toordinal()

        result = self.symbol_request_on_date(self.DAILY_URL, symbol, date, force_reload=force_reload)
        return result

    def get_data_window(self, symbol, date, window):
        if isinstance(date, dt.date):
            date = date.toordinal()

        # try the cache for the last day of the window (i.e. latest in time)
        # if the data is there for that date, we should be good for all the other dates
        cached_date = self._try_cache(symbol, date)
        if cached_date is None:
            # if the date isn't there, we need to request to repopulate the cache
            self.get_symbol_on_date(symbol, date=date)

        # finally we can get our data
        result = self._cache.get_rolling_window_quotes(symbol, date, window)
        return self.covert_to_array_of_dicts(result)

    def symbol_request_on_date(self, url, symbol, date, retries=0, force_reload=False):
        api_url = url.replace('__SYMBOL__', symbol)
        result = self._try_cache(symbol, date)

        # if we've never retrieved for the ticker, set its last retrieved to -1 so the < op doesn't blow up
        last_retrieved = self._cache.get_last_retrieved(symbol)
        if last_retrieved is None:
            last_retrieved = -1

        if (result is None or force_reload) and last_retrieved <= date:
            if force_reload:
                print('Forcing cache flush for %s' % (symbol,))

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

            self._store_data(symbol, result, force_reload=force_reload)
            self._store_meta_data(symbol)

        return result

    # Stores the actual data we receive from Alpha Vantage into the cache
    def _store_data(self, symbol, result, force_reload=False):
        if force_reload:
            print('Flushing cache for %s' % (symbol,))
            self._cache.flush(symbol)

        last_retrieved_date = self._cache.get_last_retrieved(symbol)
        daily_time_series = result['Time Series (Daily)']
        for key in daily_time_series:
            a = ()
            for item in daily_time_series[key]:
                a = a + (daily_time_series[key][item],)

            date_string = key
            year_time_series = int(date_string[0:4])
            month_time_series = int(date_string[5:7])
            day_time_series = int(date_string[8:10])
            key_date = dt.date(year_time_series, month_time_series, day_time_series).toordinal()
            if last_retrieved_date is not None and force_reload is not True:
                print("In cache, updating")
                if key_date >= last_retrieved_date:
                    print("Storing data")
                    self._cache.store_result_data(symbol, key_date, a)
                else:
                    print("Either not valid date, or past last retrieved")
                    break
            else:
                print("Not in cache, loading now")
                self._cache.store_result_data(symbol, key_date, a)

    def _store_meta_data(self, symbol):
        return self._cache.store_result_meta_data(symbol, dt.date.today().toordinal())

    # Checks cache for symbol on specific date
    def _try_cache(self, symbol, date):
        result = self._cache.check_cache(symbol, date)
        if result is not None:
            print('Found data in cache!')
            return result

        return None

    @staticmethod
    def covert_to_array_of_dicts(array):
        to_return = []
        if array is None:
            return to_return

        for item in array:
            to_return.append({
                'ticker': item[0],
                'date': item[1],
                'open': item[2],
                'high': item[3],
                'low': item[4],
                'close': item[5],
                'volume': item[6]
            })

        return to_return
