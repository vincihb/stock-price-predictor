import sqlite3
import os.path as path


class SqlExecutor:
    def __init__(self):
        self._local_dir = path.dirname(path.abspath(__file__))
        self._db_path = path.join(self._local_dir, '..', 'data', 'sqlite', 'gpp-core.db')

        db_exists = path.isfile(self._db_path)

        self.db = sqlite3.connect(self._db_path)
        # load in the database if one doesn't exist before
        if not db_exists:
            self._exec_core()

    def _exec_core(self):
        cursor = self.db.cursor()
        with open(path.join(self._local_dir, '..', 'data', 'sqlite', 'sql', 'data_core.sql')) as sql:
            cursor.executescript(sql.read())
            cursor.close()

    def exec_select(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
