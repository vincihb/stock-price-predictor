from datetime import date as dt


class DateUtil:
    @staticmethod
    def is_today(date):
        return date == dt.today().toordinal()

    @staticmethod
    def dates_match(d1, d2):
        return d1 == d2

    # TODO: fix
    @staticmethod
    def is_weekend(date):
        return False
