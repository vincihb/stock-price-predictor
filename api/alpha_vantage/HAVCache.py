import datetime
from db.SqlExecutor import SqlExecutor

class HAVCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_result_meta_data(self, ticker, last_retrieved):
        sql = 'INSERT INTO `HISTORIC_META_DATA` (TICKER, LAST_RETRIEVED) VALUES (?, ?)'
        self.db.exec_insert(sql, (ticker, last_retrieved))

    def store_result_data(self, ticker, date, payload):
        sql = 'INSERT INTO `HISTORIC_DATA` (TICKER, DATE, PAYLOAD) VALUES(?, ?, ?)'
        self.db.exec_insert(sql, (ticker, date, payload))

    def check_cache(self, ticker, date):
        sql = 'SELECT * FROM `HISTORIC_META_DATA` WHERE TICKER=?'
        result = self.db.exec_select(sql, (ticker, date)).fetchone()
        if result is None:
            return None

        found_timestamp = datetime.datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S")
        if found_timestamp.toordinal() < date.toordinal():
            return None

        result = self.get_daily_quote(ticker, date)
        return {'ticker': result[0], 'date': result[1], 'payload': result[2]}

    def get_daily_quote(self, ticker, date):
        sql = 'SELECT * FROM `HISTORIC_DATA` WHERE TICKER=? AND DATE=?'
        result = self.db.exec_select(sql, (ticker, date)).fetchone()
        return result
