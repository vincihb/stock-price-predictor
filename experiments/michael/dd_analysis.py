from datetime import date
from api.reddit.wsb.DailyDiscussion import DailyDiscussion
from api.alpha_vantage.HistoricAlphaVantageAPI import HistoricAlphaVantageAPI


def generate_report():
    # lets examine statistics for the last 3 weeks of 3 large indices (Nasdaq, S+P 500, DJIA)
    for_date = date.today().toordinal()
    spy = HistoricAlphaVantageAPI().get_data_window('SPY', for_date, 15)
    dow = HistoricAlphaVantageAPI().get_data_window('DOW', for_date, 15)
    qqq = HistoricAlphaVantageAPI().get_data_window('QQQ', for_date, 15)

    print(spy)
    print(dow)
    print(qqq)


generate_report()
