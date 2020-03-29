from api.reddit.HistoricRedditAPI import HistoricRedditAPI
from api.alpha_vantage import HistoricAlphaVantageAPI
import datetime as dt
from nlu.SentimentAnalyzer import SentimentAnalyzer
from client.util.html.TableBuilder import TableBuilder
from client.Reporter import Reporter

start_date = dt.datetime(2020, 1, 1)
end_date = dt.datetime(2020, 3, 15)

historic_reddit = HistoricRedditAPI()
historic_reddit.set_subreddit('wallstreetbets')
historic_reddit.set_limit(100)
historic_reddit.set_start_epoch(start_date)
historic_reddit.set_end_date(end_date)
historic_posts = historic_reddit.get_something()

historic_buffer_size = 10

list_of_stocks_and_scores = SentimentAnalyzer.get_net_sentiment_historic(historic_posts)

print(list_of_stocks_and_scores)

historic_stock_pricing = HistoricAlphaVantageAPI.HistoricAlphaVantageAPI()
table_values = []

for stock in list_of_stocks_and_scores:
    ticker = stock[0]
    ticker_data = historic_stock_pricing.get_data_window(ticker, end_date, historic_buffer_size)
    if len(ticker_data) > 0:
        first_date_data = ticker_data[0]
        end_date_data = ticker_data[historic_buffer_size - 1]
        difference_data = float(first_date_data['open']) - float(end_date_data['close'])
        print("Ticker: %s, sentiment: %f, result: %f" % (ticker, stock[1], difference_data))
        table_values.append([ticker, stock[1], difference_data])


def generate_report():
    # Build the actual report from our parsed data
    report = Reporter()
    report.set_title('Historic Sensitivity Report')

    # set up a table
    table_header = ['Ticker', 'Sentiment', '10 day Result']
    report.set_body(TableBuilder(headers=table_header, rows=table_values))

    report.compile()

    return report.title


generate_report()