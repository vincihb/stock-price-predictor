import sqlite3
import os.path as path


class SqlExecutor:
    def __init__(self, debug=False):
        self._local_dir = path.dirname(path.abspath(__file__))
        self._db_path = path.join(self._local_dir, '..', 'data', 'sqlite', 'gpp-core.db')
        self.debug = debug

        db_exists = path.isfile(self._db_path)

        self.db = sqlite3.connect(self._db_path)
        # load in the database if one doesn't exist before
        if not db_exists:
            self._exec_core()

        self.is_closed = False

    def _exec_core(self):
        cursor = self.db.cursor()
        with open(path.join(self._local_dir, '..', 'data', 'sqlite', 'sql', 'data_core.sql')) as sql:
            cursor.executescript(sql.read())

    def exec_select(self, sql):
        if self.is_closed:
            return None

        if self.debug:
            print(sql)

        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor

    def exec_insert(self, sql, with_params=None):
        if self.debug:
            print(sql)

        cursor = self._exec_sql(sql, with_params)
        return cursor.lastrowid

    def _exec_sql(self, sql, with_params):
        if self.is_closed:
            return None

        cursor = self.db.cursor()
        with self.db:
            if with_params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, with_params)

        return cursor

    def close(self):
        self.db.close()
        self.is_closed = True

