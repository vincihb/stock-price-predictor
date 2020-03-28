from client.util.html.tooling.base.HTMLElement import HTMLElement
from client.util.html.tooling.table.TableCellElement import TableCellElement
from client.util.html.tooling.table.TableHeaderElement import TableHeaderElement
from client.util.html.tooling.table.TableBodyElement import TableBodyElement
from client.util.html.tooling.table.TableFooterElement import TableFooterElement
from client.util.html.tooling.table.TableRowElement import TableRowElement


class TableElement(HTMLElement):
    def __init__(self):
        super().__init__('table')

        self.header = TableHeaderElement()
        self.body = TableBodyElement()
        self.footer = TableFooterElement()

        self.append_child(self.header)
        self.append_child(self.body)
        self.append_child(self.footer)

    # convenience methods that don't exist in HTML
    def set_column_headers(self, column_labels=None):
        if column_labels is None:
            column_labels = []

        for label in column_labels:
            self.header.add_column_header(label)

    def add_row(self, row_data=None):
        if row_data is None:
            row_data = []

        row = TableRowElement()
        for cell in row_data:
            row.append_child(TableCellElement(text=cell))

        self.body.append_child(row)

    def add_multiple_rows(self, all_rows=None):
        if all_rows is None:
            all_rows = [[]]

        for row in all_rows:
            self.add_row(row)
