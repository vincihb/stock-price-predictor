from client.util.html.tooling.base.HTMLElement import HTMLElement


class TableHeaderCellElement(HTMLElement):
    def __init__(self, text=''):
        super().__init__('th')
        self.set_inner_text(text)
