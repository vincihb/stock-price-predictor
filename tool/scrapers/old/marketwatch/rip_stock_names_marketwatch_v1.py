"""This is V1, V2 will scrape more information, such as the description__text class information"""

import requests as req
import os
import time

with open('../../../../data/tickers/compiled/all_tickers.txt') as ticker_file:
    with open('../../data/tickers/compiled/tickers_named.txt', 'w') as ticker_file_out:
        for ticker in ticker_file:
            ticker = ticker[:-1]

            result = req.get('https://www.marketwatch.com/investing/stock/' + ticker)
            out = os.popen('curl -s https://www.marketwatch.com/investing/stock/' + ticker +
                           ' | grep \'class="company__name"\'| sed -e "s/<[^>]*>//g"')

            proper_name = out.read().strip()
            print(ticker + '=' + proper_name + '\n')
            ticker_file_out.write(ticker + '=' + proper_name + '\n')
            time.sleep(0.2)
