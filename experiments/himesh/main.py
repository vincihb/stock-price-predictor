from api.reddit.HistoricRedditAPI import HistoricRedditAPI
from api.alpha_vantage import HistoricAlphaVantageAPI
import datetime as dt
from nltk.stem.snowball import SnowballStemmer
from nlu.SentimentAnalyzer import SentimentAnalyzer

historic_reddit = HistoricRedditAPI()
historic_reddit.set_subreddit('wallstreetbets')
historic_reddit.set_limit(10)
historic_reddit.set_start_epoch(dt.datetime(2019, 1, 1))
historic_reddit.set_end_date(dt.datetime(2019, 2, 28))
historic_posts = historic_reddit.get_something()
tickers_found = {}
stemmer = SnowballStemmer("english")

historic_stock_pricing = HistoricAlphaVantageAPI.HistoricAlphaVantageAPI()
print(dt.date(2020, 1, 1).toordinal())
a = historic_stock_pricing.get_symbol_on_date('TSLA', dt.date(2019, 2, 15))
print(a)
b = historic_stock_pricing.get_data_window('TSLA', dt.date(2019, 2, 17), 5)
print(b)

list_of_stocks_and_scores = SentimentAnalyzer.get_net_sentiment_historic(historic_posts)

print(list_of_stocks_and_scores)