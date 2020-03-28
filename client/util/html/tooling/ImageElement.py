from client.util.html.tooling.base.Attributes import Attributes
from client.util.html.tooling.base.HTMLElement import HTMLElement


class ImageElement(HTMLElement):
    def __init__(self, src, alt):
        super().__init__('img')

        self.set_attribute(Attributes.SRC, src)
        self.set_attribute(Attributes.ALT, alt)

