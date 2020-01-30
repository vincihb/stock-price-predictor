import re
import time

from api.local_stocks.Ticker import Ticker
from api.reddit.RedditAPI import RedditAPI
from api.alpha_vantage.AlphaVantageAPI import AlphaVantageAPI
from nlu.NLTKUtil import NLTKUtil
from client.Reporter import Reporter
from client.util.HTMLUtil import HTMLUtil
from client.util.ChartBuilder import ChartBuilder
from client.util.charts.DataSet import DataSet
from client.util.html.TableBuilder import TableBuilder
from client.util.html.LinkBuider import LinkBuilder
from client.util.html.ScrollableDiv import ScrollableDiv

# gather the current top 50 posts from WSB
reddit = RedditAPI()
submissions = reddit.get_hot('wallstreetbets', limit=1000)

# loop through and try to pick out tickers
tickers_found = {}
for sub in range(0, len(submissions['title'])):
    title = submissions['title'][sub]
    self_text = submissions['body'][sub]
    url = submissions['url'][sub]
    score = submissions['score'][sub]

    ticker = None
    sorted_bow = NLTKUtil.get_weighted_stock_count(title, self_text)
    for word in sorted_bow:
        match = re.search('[A-Z]{2,4}', word)
        if match is not None:
            match_result = match.group(0).strip()
            t = Ticker()
            result = t.get_ticker(match_result.upper())
            if result is not None:
                ticker = result
                break

    if ticker is None:
        continue

    ticker_symbol = ticker[0]

    # if it is, write down information about the ticker and how many times we've seen it
    if ticker_symbol in tickers_found:
        tickers_found[ticker_symbol]['count'] += 1
        tickers_found[ticker_symbol]['submissions'].append({'link': url, 'title': title, 'score': score})
    else:
        tickers_found[ticker_symbol] = {
            'count': 1,
            'submissions': [{'link': url, 'title': title, 'score': score}],
            'name': LinkBuilder(ticker[1], ticker[-3]),
            'description': ticker[2]
        }


def sort_dict_by_score(item):
    return item['score']


def sort_by_mentions(item):
    return item[1]


# sort the submissions by score
for tf in tickers_found:
    tickers_found[tf]['submissions'].sort(reverse=True, key=sort_dict_by_score)

# then reformat the result so that we can put it in a tabular format
table_values = []
for tf in tickers_found:
    addendum = ''
    counter = 0
    for submission in tickers_found[tf]['submissions']:
        addendum += LinkBuilder('[%d] - %d' % (counter, submission['score']), submission['link']).compile() + '<br />'
        counter += 1

    addendum = ScrollableDiv(addendum, '5rem').compile()

    desc = '...'
    if 'description' in tickers_found[tf] and tickers_found[tf]['description'] is not None:
        desc = tickers_found[tf]['description']

    if tickers_found[tf]['count'] > 2:
        print('crawling AV for %s' % tf)
        pct_change = AlphaVantageAPI().get_quote(tf)['10. change percent']
        pct_in_tag = HTMLUtil.wrap_in_tag(pct_change, 'div', attributes={'class': 'negative' if '-' in pct_change else 'positive'})
    else:
        pct_in_tag = 'N/A'

    table_values.append([tf, tickers_found[tf]['count'], tickers_found[tf]['name'],
                         desc[:200] + '...', pct_in_tag, addendum])

    time.sleep(20)

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
report.set_title('NLU Report')

# set up a table
table_header = ['Ticker', 'Mentions', 'Name', 'Description', 'Movement', 'Links']
report.set_body(TableBuilder(headers=table_header, rows=table_values))

# and a chart
report.append_to_body(ChartBuilder(title='WSB Mentions', chart_type='bar', data_set=ds))
report.compile()
