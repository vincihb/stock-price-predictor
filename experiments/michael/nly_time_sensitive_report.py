from api.reddit.RedditAPI import RedditAPI
from client.Reporter import Reporter
from client.util.ChartBuilder import ChartBuilder
from client.util.charts.DataSet import DataSet
from client.util.html.LinkBuider import LinkBuilder
from experiments.michael.AlbinsonianHTML import AlbinsonianHTML
from nlu.NLUSubjectTickerEstimator import NLUSubjectTickerEstimator
from reports.Sorting import Sorting

REPORT_TITLE = "NLU - Time Sensitive"
TRIM_THRESH = 10
FORCE_CACHE_RELOAD = False


def generate_report(table_date=None):
    reddit = RedditAPI()
    epochs = reddit.get_new('wallstreetbets', limit=1000, cast_to='epoch')

    epoch_meta = {}
    most_recent_date = None
    epoch_count = 0
    for epoch in epochs:
        epoch_count += 1
        if most_recent_date is None:
            most_recent_date = epoch

        epoch_data = epochs[epoch]

        if epoch == table_date:
            print(epoch_data)

        tickers_found = {}
        total_posts = 0
        for sub in epoch_data:
            total_posts += 1
            ticker = NLUSubjectTickerEstimator.estimate(sub['title'], sub['body'])

            if ticker is None:
                continue

            ticker_symbol = ticker[0]
            url = sub['url']
            title = sub['title']
            score = sub['score']

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

        # sort the tickers we found
        for tf in tickers_found:
            tickers_found[tf]['submissions'].sort(reverse=True, key=Sorting.sort_by_score)

        tickers_found = {k: v for k, v in sorted(tickers_found.items(), key=lambda it: it[1]['count'], reverse=True)}

        epoch_meta[epoch] = {'tickers': tickers_found, 'post_count': total_posts}

    table = ''
    print(epoch_meta)
    x = []
    y_dict = {}
    ds = DataSet()
    epoch_counter = 0
    for meta in epoch_meta:
        epoch_counter += 1
        metadata = epoch_meta[meta]

        # if you specify a date, allow generating a table for dates in the past
        if table_date is None and meta == most_recent_date:
            table = AlbinsonianHTML.get_ticker_table(metadata['tickers'], force_reload=FORCE_CACHE_RELOAD)
        elif table_date is not None and table_date == meta:
            table = AlbinsonianHTML.get_ticker_table(metadata['tickers'], force_reload=FORCE_CACHE_RELOAD)

        x.append(meta)
        for ticker in metadata['tickers']:
            ticker_meta = metadata['tickers'][ticker]

            if ticker in y_dict:
                y_dict[ticker].append(ticker_meta['count'])
            else:
                # correct if a ticker was missing for a few epochs, but then blips in
                y_dict[ticker] = [0] * (epoch_counter - 1)
                y_dict[ticker].append(ticker_meta['count'])

        for ticker in y_dict:
            if len(y_dict[ticker]) < epoch_counter:
                y_dict[ticker].append(0)

    x.reverse()
    ds.set_x(x)
    for ticker_ds in y_dict:
        ticker_data = y_dict[ticker_ds]
        if len(ticker_data) < epoch_count or sum(ticker_data) < TRIM_THRESH:
            continue

        ticker_data.reverse()
        ds.append_y_set({"label": ticker_ds, "data": ticker_data})

    report = Reporter()
    report.set_title(REPORT_TITLE)
    report.append_to_body(table, section_id='ticker-table')
    report.append_to_body(ChartBuilder(title="Mentions over Time", data_set=ds, chart_type='line'))
    report.compile()

    return report.title
