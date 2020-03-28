from client.util.html.tooling.base.HTMLElement import HTMLElement


class StrongElement(HTMLElement):
    def __init__(self, text=''):
        super().__init__('strong')

        self.set_inner_text(text)
