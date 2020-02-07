from api.reddit.HistoricRedditAPI import HistoricRedditAPI
from api.alpha_vantage import HistoricAlphaVantageAPI
from nlu.NLTKUtil import NLTKUtil
import datetime as dt
from nltk.stem.snowball import SnowballStemmer
from os import path

historic_reddit = HistoricRedditAPI()
historic_reddit.set_subreddit('wallstreetbets')
historic_reddit.set_limit(10)
historic_reddit.set_start_epoch(dt.datetime(2020,1,1))
historic_reddit.set_end_date(dt.datetime(2020,1,5))
c = historic_reddit.get_something()
tickers_found = {}
stemmer = SnowballStemmer("english")

historic_stock_pricing = HistoricAlphaVantageAPI.HistoricAlphaVantageAPI()
print(dt.date(2020, 1, 1).toordinal())
a = historic_stock_pricing.get_symbol_on_date('TSLA', dt.date(2019, 2, 15).toordinal())
print(a)
exit()

PATH = path.dirname(path.abspath(__file__))
PATH_POSITIVE = path.join(PATH, '..', '..', 'data', 'jargon', 'positive.txt')
print(PATH_POSITIVE)
with open(PATH_POSITIVE) as file_data:
    positive_stemmed_list = [stemmer.stem(line.strip()) for line in file_data]
    unique_positive_stemmed_words = list(set(positive_stemmed_list))

PATH_NEGATIVE = path.join(PATH, '..', '..', 'data', 'jargon', 'negative.txt')
with open(PATH_NEGATIVE) as file_data:
    negative_stemmed_list = [stemmer.stem(line.strip()) for line in file_data]
    unique_negative_stemmed_words = list(set(negative_stemmed_list))


PATH_NOT_TICKERS = path.join(PATH, '..', '..', 'data', 'jargon', 'not_tickers.txt')
with open(PATH_NOT_TICKERS) as file_data:
    not_tickers_list = [line.strip() for line in file_data]

list_of_stocks_and_scores = []

for submission in c:
    title = submission.title
    body = submission.selftext
    print("###################")
    print("TITLE: " + str(title))
    print(body)
    bow = NLTKUtil.get_weighted_stock_count(title, body)
    score = 0
    positive_match = 0
    negative_match = 0

    ticker = NLTKUtil.get_likely_subject_stock(bow)

    if ticker is not None:
        ticker_symbol = ticker[0]
        print(ticker_symbol)
    else:
        continue

    for word in bow.keys():
        for positive_stem in unique_positive_stemmed_words:
            if positive_stem in word.lower():
                positive_match += bow[word]

        for negative_stem in unique_negative_stemmed_words:
            if negative_stem in word.lower():
                negative_match += bow[word]

    print("Positive match: " + str(positive_match))
    print("Negative match: " + str(negative_match))
    score = positive_match - negative_match
    print("Score: " + str(score))

    list_of_stocks_and_scores.append((ticker_symbol, score))

