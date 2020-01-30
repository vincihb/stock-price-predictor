from db.SqlExecutor import SqlExecutor


class AVCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_result(self, ticker, req_class, payload):
        sql = 'INSERT INTO `AV_CACHE` (TICKER, CLASS, PAYLOAD) VALUES (?, ?, ?)'
        self.db.exec_insert(sql, (ticker, req_class, payload))

    def check_cache(self, ticker, req_class):
        sql = 'SELECT * FROM `AV_CACHE` WHERE TICKER=? and CLASS=?'
        self.db.exec_select(sql, (ticker, req_class))