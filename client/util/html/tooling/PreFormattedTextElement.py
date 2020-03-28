from client.util.html.tooling.base.HTMLElement import HTMLElement


class PreFormattedTextElement(HTMLElement):
    def __init__(self, text=''):
        super().__init__('pre')
        self.set_inner_text(text)
