import re

from api.local_stocks.Ticker import Ticker
from api.reddit.RedditAPI import RedditAPI
from client.Reporter import Reporter
from client.util.ChartBuilder import ChartBuilder
from client.util.charts.DataSet import DataSet
from client.util.html.TableBuilder import TableBuilder
from client.util.html.LinkBuider import LinkBuilder

# gather the current top 50 posts from WSB
reddit = RedditAPI()
submissions = reddit.get_hot('wallstreetbets', limit=50)

# loop through and try to pick out tickers
tickers_found = {}
for sub in range(0, len(submissions['title'])):
    title = submissions['title'][sub]
    self_text = submissions['body'][sub]
    url = submissions['url'][sub]

    match = re.search('[A-Z]{2,4}', title + self_text)
    if match is not None:
        ticker = match.group(0).strip()

        # if we get a match, verify that it's a real ticker
        t = Ticker()
        result = t.get_ticker(ticker)
        if result is None:
            continue

        # if it is, write down information about the ticker and how many times we've seen it
        if ticker in tickers_found:
            tickers_found[ticker]['count'] += 1
            tickers_found[ticker]['links'].append(url)
            tickers_found[ticker]['titles'].append(title)
        else:
            tickers_found[ticker] = {
                'count': 1,
                'links': [submissions['url'][sub]],
                'titles': [title],
                'name': LinkBuilder(result[1], result[-3]),
                'description': result[2]
            }


def sort_by_mentions(a):
    return a[1]

# then reformat the result so that we can put it in a tabular format
table_values = []
for ticker in tickers_found:
    table_values.append([ticker, tickers_found[ticker]['count'], tickers_found[ticker]['name'],
                         tickers_found[ticker]['description'][:200] + '...'])

table_values.sort(key=sort_by_mentions, reverse=True)

# and then mutate the data again to match the data format for bar charts
x = []
y = []
for arr in table_values:
    x.append(arr[0])
    y.append(arr[1])

ds = DataSet()
ds.set_x(x)
ds.append_y_set({'data': y, 'label': ''})

# Build the actual report from our parsed data
report = Reporter()
report.set_title('Sample Wall Street Bets Report')

# set up a table
table_header = ['Ticker', 'Mentions', 'Name', 'Description']
report.set_body(TableBuilder(headers=table_header, rows=table_values))

# and a chart
report.append_to_body(ChartBuilder(title='WSB Mentions', chart_type='bar', data_set=ds))
report.compile()
