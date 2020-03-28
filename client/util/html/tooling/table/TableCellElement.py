from client.util.html.tooling.base.HTMLElement import HTMLElement


class TableCellElement(HTMLElement):
    def __init__(self, text=''):
        super().__init__('td')
        self.set_inner_text(text=str(text))
