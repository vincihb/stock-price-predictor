from client.util.html.tooling.base.Attributes import Attributes
from client.util.html.tooling.base.HTMLElement import HTMLElement


class LinkElement(HTMLElement):
    def __init__(self, text, href, target=None):
        super().__init__('a')

        self.set_inner_text(text)
        self.set_attribute(Attributes.HREF, href)
        if target is not None:
            self.set_attribute(Attributes.TARGET, target)
