from client.util.html.tooling.base.HTMLElement import HTMLElement


class CodeElement(HTMLElement):
    def __init__(self, text=''):
        super().__init__('code')
        self.set_inner_text(text)
