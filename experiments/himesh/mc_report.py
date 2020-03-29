from util.MarkovChain import MarkovChain
from client.util.ChartBuilder import ChartBuilder
from client.util.HTMLUtil import HTMLUtil
from client.Reporter import Reporter
from client.util.charts.DataSet import DataSet
from api.reddit.wsb.DailyDiscussion import DailyDiscussion
from api.alpha_vantage.AlphaVantageAPI import AlphaVantageAPI
import datetime as dt
import collections


def generate_report():
    dd_object = DailyDiscussion()
    alpha_vantage = AlphaVantageAPI()
    tickers = dd_object.get_daily_discussion(for_date=dt.date.today())
    temp_dict = {k: v['count'] for (k, v) in tickers[0].get('tickers').items() if k != 'misc'}
    c = collections.Counter(temp_dict)
    report = Reporter()
    report.set_title('Markov Chain Report')
    for tuple_c in c.most_common(20):
        ticker = tuple_c[0]
        mc = MarkovChain(ticker)
        mc.build_markov_chain()
        x, y = mc.predict()
        if x is None or y is None:
            continue
        mu = mc.expected_value(x, y)
        var = mc.var(x, y)
        prev_day_change = alpha_vantage.get_quote(ticker)
        prev_day_change = prev_day_change['Global Quote']['10. change percent']
        ds = DataSet()
        ds.set_x(x.tolist())
        ds.append_y_set({'data': y.tolist(), 'label': ''})
        report.append_to_body(ChartBuilder(title='Markov Chain: ' + ticker, chart_type='line', data_set=ds, y_label=ticker))
        report.append_to_body(HTMLUtil.wrap_in_tag("Expected Value: " + str(round(mu, 3)) + "%", 'p'))
        report.append_to_body(HTMLUtil.wrap_in_tag("Variance: " + str(round(var, 3)) + "%", 'p'))
        report.append_to_body(HTMLUtil.wrap_in_tag("Previous day's change: " + prev_day_change, 'p'))
    report.compile()
    return report.title


if __name__ == "__main__":
    generate_report()