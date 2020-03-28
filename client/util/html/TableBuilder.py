from client.util.html.tooling.table.TableElement import TableElement

BASE_INDENT = 3


class TableBuilder:
    def __init__(self, headers=None, rows=None):
        if rows is None:
            rows = [[]]

        if headers is None:
            headers = []

        self._table = TableElement()
        self._table.set_column_headers(headers)
        self._table.add_multiple_rows(rows)

    def compile(self):
        return self._table.render(indent=BASE_INDENT)

    def __str__(self):
        return self.compile()
