from client.util.html.tooling.base.HTMLElement import HTMLElement
from client.util.html.tooling.table.TableHeaderCellElement import TableHeaderCellElement


class TableHeaderElement(HTMLElement):
    def __init__(self):
        super().__init__('thead')

    def add_column_header(self, text):
        self.append_child(TableHeaderCellElement(text))