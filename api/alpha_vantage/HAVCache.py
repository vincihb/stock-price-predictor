import datetime
from db.SqlExecutor import SqlExecutor


class HAVCache:
    def __init__(self):
        self.db = SqlExecutor(db_name='gpp-long-term.db')

    def store_result_meta_data(self, ticker, last_retrieved):
        sql = 'SELECT * FROM `HISTORIC_META_DATA` WHERE TICKER=?'
        found = self.db.exec_select(sql, (ticker,))
        # if there's already a metadata record, just update it
        if found is not None:
            sql = 'UPDATE `HISTORIC_META_DATA` SET LAST_RETRIEVED=? WHERE TICKER=?'
            self.db.exec_select(sql, (last_retrieved, ticker))
        else:
            sql = 'INSERT INTO `HISTORIC_META_DATA` (TICKER, LAST_RETRIEVED) VALUES (?, ?)'
            self.db.exec_insert(sql, (ticker, last_retrieved))

    def store_result_data(self, ticker, date, payload):
        sql = 'INSERT INTO `HISTORIC_DATA` (TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?)'
        to_send = (ticker, date)
        for item in payload:
            to_send = to_send + (item,)

        self.db.exec_insert(sql, to_send)

    # Checks whether specific date is actually in the cache
    def check_cache(self, ticker, date):
        found_timestamp = self.get_last_retrieved(ticker)
        if found_timestamp is None or found_timestamp < date:
            return None

        result = self.get_daily_quote(ticker, date)
        if result is None:
            return None

        return {'ticker': result[0], 'date': result[1], 'open': result[2],
                'high': result[3], 'low': result[4], 'close': result[5], 'volume': result[6]}

    def get_last_retrieved(self, ticker):
        sql = 'SELECT * FROM `HISTORIC_META_DATA` WHERE TICKER=?'
        result = self.db.exec_select(sql, (ticker,)).fetchone()
        if result is None:
            return None

        found_timestamp = result[1]
        return found_timestamp

    def get_rolling_window_quotes(self, ticker, ord_date, num_desired):
        sql = 'SELECT * FROM `HISTORIC_DATA` WHERE TICKER=? AND DATE <= ? ORDER BY DATE DESC LIMIT ?'
        result = self.db.exec_select(sql, (ticker, ord_date, num_desired)).fetchall()
        return result

    def get_time_data(self, ticker):
        sql = 'SELECT * FROM `HISTORIC_DATA` WHERE TICKER=?'

    def get_daily_quote(self, ticker, date):
        sql = 'SELECT * FROM `HISTORIC_DATA` WHERE TICKER=? AND DATE=?'
        result = self.db.exec_select(sql, (ticker, date)).fetchone()
        return result

    def flush(self, ticker):
        sql = 'DELETE FROM `HISTORIC_DATA` WHERE TICKER=?'
        self.db.exec_insert(sql, (ticker,))

