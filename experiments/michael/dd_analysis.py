from datetime import date
from api.reddit.wsb.DailyDiscussion import DailyDiscussion


def generate_report():
    todays_dd = DailyDiscussion().get_daily_discussion(for_date=date.today())
    todays_dd_tickers = todays_dd[0]['tickers']
    print(todays_dd_tickers)

    DailyDiscussion().get_n(n=5)

    tickers_found = {k: v for k, v in sorted(todays_dd_tickers.items(), key=lambda it: it['count'], reverse=True)}

    print(tickers_found)


generate_report()
