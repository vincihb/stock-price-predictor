from datetime import date
from api.reddit.wsb.DailyDiscussion import DailyDiscussion
from client.Reporter import Reporter
from client.util.ChartBuilder import ChartBuilder
from client.util.charts.DataSet import DataSet
from nlu.SentimentAnalyzer import SentimentAnalyzer
from api.alpha_vantage.HistoricAlphaVantageAPI import HistoricAlphaVantageAPI


def get_net_change(spy, dow, qqq):
    def pct_move(day):
        return ((float(day['close']) - float(day['open'])) / float(day['open'])) * 100

    spy_chg = pct_move(spy)
    dow_chg = pct_move(dow)
    qqq_chg = pct_move(qqq)

    avg_chg = (spy_chg + qqq_chg + dow_chg) / 3

    return round(avg_chg, 4)


def generate_report():
    # lets examine statistics for the last 3 weeks of 3 large indices (Nasdaq, S+P 500, DJIA)
    for_date = date.today().toordinal() - 1
    spy = HistoricAlphaVantageAPI().get_data_window('SPY', for_date, 15)
    dow = HistoricAlphaVantageAPI().get_data_window('DOW', for_date, 15)
    qqq = HistoricAlphaVantageAPI().get_data_window('QQQ', for_date, 15)

    print(spy)
    print(dow)
    print(qqq)

    net_change = []
    dates = []
    sentiment = []
    for index in range(len(spy)):
        dates.append(str(date.fromordinal(spy[index]['date'])))
        net_change.append(get_net_change(spy[index], dow[index], qqq[index]))

        dd = DailyDiscussion().get_daily_discussion(spy[index]['date'])
        sentiment.append(SentimentAnalyzer.get_average_discussion_sentiment(dd))

    print(sentiment)
    # get the average sentiment ratio over the time period for normalization
    ratio_avg = sum([sent[2] for sent in sentiment]) / len(sentiment)

    # reverse
    dates.reverse()
    sentiment.reverse()
    net_change.reverse()

    ds = DataSet()
    ds.set_x(dates)
    ds.set_y1_name('Index % Change')
    ds.append_y_set({'data': net_change, 'label': 'Major Indices Avg Change'})
    ds.set_y2_name('Sentiment Ratio')
    ds.append_secondary_axis_y_set({'data': [sent[2] for sent in sentiment], 'label': 'WSB Sentiment'})
    ds.append_secondary_axis_y_set({'data': [ratio_avg] * len(dates), 'label': 'Average Sentiment'})

    chart = ChartBuilder(title='Major Index Change vs Sentiment', data_set=ds, x_label='Date', chart_type='line')

    # Build the actual report from our parsed data
    report = Reporter()
    report.set_title('DD Sentiment Report')
    report.set_body(chart)
    report.compile()



generate_report()
