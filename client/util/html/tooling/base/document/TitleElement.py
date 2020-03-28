from client.util.html.tooling.base.HTMLElement import HTMLElement


class TitleElement(HTMLElement):
    def __init__(self, docTitle):
        super().__init__('title')
        self.set_inner_text(docTitle)
