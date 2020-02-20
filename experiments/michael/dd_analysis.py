from datetime import date
from api.reddit.wsb.DailyDiscussion import DailyDiscussion


def generate_report():
    todays_dd = DailyDiscussion().get_daily_discussion(for_date=date.today())
    print(len(todays_dd))
    print(todays_dd[0]['tickers'].keys())


generate_report()
