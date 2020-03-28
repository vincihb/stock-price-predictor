from client.util.html.tooling.base.HTMLElement import HTMLElement


class HeaderElement(HTMLElement):
    def __init__(self, level, text):
        super().__init__('h' + str(level))
        self.set_inner_text(text)
