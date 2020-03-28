from client.util.html.tooling.base.HTMLElement import HTMLElement


class SpanElement(HTMLElement):
    def __init__(self, text=''):
        super().__init__('span')
        self.set_inner_text(text)
