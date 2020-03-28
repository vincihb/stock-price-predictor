from client.util.html.tooling.base.HTMLElement import HTMLElement


class DivElement(HTMLElement):
    def __init__(self, text=''):
        super().__init__('div')
        self.set_inner_text(text)
