
from client.util.html.tooling.DivElement import DivElement
from client.util.html.tooling.base.Attributes import Attributes


class ScrollableDiv:
    def __init__(self, body, max_height, indent=5, min_width='10rem'):
        self._div = DivElement(text=body)
        self._div.set_attribute(Attributes.STYLE, "max-height: " + max_height + "; overflow: auto; min-width: " + min_width + ";")
        self._indent = indent

    def compile(self):
        return self._div.render(indent=self._indent)
