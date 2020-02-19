import datetime
from db.SqlExecutor import SqlExecutor


class AVCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_result(self, ticker, req_class, payload):
        sql = 'INSERT INTO `AV_CACHE` (TICKER, CLASS, PAYLOAD) VALUES (?, ?, ?)'
        self.db.exec_insert(sql, (ticker, req_class, payload))

    def check_cache(self, ticker, req_class, force_reload=False):
        sql = 'SELECT * FROM `AV_CACHE` WHERE TICKER=? and CLASS=?'
        result = self.db.exec_select(sql, (ticker, req_class)).fetchone()
        if result is None:
            return None

        # if the data is not from today, delete it and return none
        if datetime.datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S").day != datetime.date.today().day or force_reload:
            self.delete_old(ticker, req_class)
            return None

        return {'ticker': result[0], 'payload': result[2]}

    def delete_old(self, ticker, req_class):
        sql = 'DELETE FROM `AV_CACHE` WHERE TICKER=? and CLASS=?'
        self.db.exec_insert(sql, (ticker, req_class))
