import hashlib
import datetime

from db.SqlExecutor import SqlExecutor

'''
Some APIs have internal monitoring (cough AlphaVantage cough NewsAPI) of API calls per day for free users, this class is
to help developers have an understanding of how many calls ave been executed for a give API per day
'''


class APIUsageTracker:
    def __init__(self):
        self._executor = SqlExecutor()

    def get_use_count(self, key):
        api_key_hash = self.hash_key(key)
        result = self._executor.exec_select('SELECT * FROM `API_META` WHERE API_KEY=?', (api_key_hash,)).fetchone()
        if result is None:
            return None
        else:
            # if the data is not from today, delete it
            if datetime.datetime.strptime(result[2]).day != datetime.date.today().day:
                self._executor.exec_insert('DELETE FROM `API_META` WHERE API_KEY=?', (api_key_hash,))
                return None

            return result[1]

    def update_use_count(self, key, value):
        api_key_hash = self.hash_key(key)
        result = self.get_use_count(key)
        if result is None:
            self._executor.exec_insert('INSERT INTO `API_META` (API_KEY, USAGES) VALUES (?, ?)', (api_key_hash, value))
        else:
            self._executor.exec_insert('UPDATE `API_META` SET USAGES=? WHERE API_KEY=?', (value, api_key_hash))

        return value

    @staticmethod
    def hash_key(key):
        key = key.encode('utf-8')
        m = hashlib.md5()
        m.update(key)
        return m.hexdigest()
