from datetime import date as dt
from datetime import datetime as dtime


class DateUtil:
    @staticmethod
    def is_today(date):
        if isinstance(date, dt) or isinstance(date, dtime):
            date = date.toordinal()
        return date == dt.today().toordinal()

    @staticmethod
    def dates_match(d1, d2):
        if not isinstance(d1, dt) and not isinstance(d2, dt) \
                and not isinstance(d1, dtime) and not isinstance(d2, dtime):
            return d1 == d2
        if isinstance(d1, dt) or isinstance(d1, dtime):
            d1 = d1.toordinal()
        if isinstance(d2, dt) or isinstance(d2, dtime):
            d2 = d2.toordinal()
        return d1 == d2

    @staticmethod
    def is_weekend(date):
        if not isinstance(date, dt) and not isinstance(date, dtime):
            date = dt.fromordinal(date)
        if date.weekday() == 5 or date.weekday() == 6:
            return True
        return False
