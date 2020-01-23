import json
import requests as req

"""Class for calling the AlphaVantage API to retrieve stock data"""


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
        with open('config/stock_api.json') as json_data:
            d = json.load(json_data)

        self.API_KEY = d['API_KEY']

    def get_intraday_data(self, symbol, interval='60min', output_size='compact'):
        prepared_url = AlphaVantageAPI.INTRADAY_URL \
            .replace('__INTERVAL__', interval) \
            .replace('__OUTPUT_SIZE__', output_size)

        return self.symbol_request(prepared_url, symbol)

    def get_quote(self, symbol):
        return self.symbol_request(AlphaVantageAPI.QUOTE_URL, symbol)

    def get_weekly_data(self, symbol):
        return self.symbol_request(AlphaVantageAPI.WEEKLY_URL, symbol)

    def get_daily_data(self, symbol):
        return self.symbol_request(AlphaVantageAPI.DAILY_URL, symbol)

    def symbol_request(self, url, symbol):
        api_url = url.replace('__SYMBOL__', symbol)
        return self.make_request(api_url)

    def make_request(self, url):
        final_url = url.replace('__API_KEY__', self.API_KEY)
        result = req.get(final_url)
        if result.status_code == req.codes.ok:
            return result.text
        else:
            return 'Error'
