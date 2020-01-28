from api.reddit.RedditAPI import RedditAPI
from api.reddit.HistoricRedditAPI import HistoricRedditAPI
from db.SqlExecutor import SqlExecutor
from tool.scrapers.util.MarketWatchScraper import MarketWatchScraper

r = HistoricRedditAPI()
r.set_subreddit('wallstreetbets')
data = r.get_something()
for el in data:
    print(el)

URL_PATTERN = 'https://www.marketwatch.com/investing/stock/$$TICKER$$/profile'
FUND_URL_PATTERN = 'https://www.marketwatch.com/investing/fund/$$TICKER$$'

TICKER_PATTERN = '$$TICKER$$'
DESCRIPTION_PATTERN = '$$DESC$$'


def split_too_long_tickers():
    e = SqlExecutor(debug=True)
    rows = e.exec_select('SELECT * FROM COMPANY WHERE NAME is NULL')
    for row in rows:
        # if the ticker is too long,
        if len(row[0]) > 4:
            ticker = row[0]
            # print(ticker)
            results = ticker.rsplit(ticker[0])
            results = results[1:]
            for result in results:
                if result != '':
                    new_name = ticker[0] + result
                    e.exec_insert("INSERT INTO `COMPANY` (`NAME`) VALUES (?)", (new_name,))
                    print(ticker[0] + result)


MarketWatchScraper().update_all_tickers()
