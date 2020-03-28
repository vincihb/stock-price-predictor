from client.util.html.tooling.base.HTMLElement import HTMLElement


class ParagraphElement(HTMLElement):
    def __init__(self, text=''):
        super().__init__('p')
        self.set_inner_text(text)
