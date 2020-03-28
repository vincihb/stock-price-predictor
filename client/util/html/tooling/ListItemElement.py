from client.util.html.tooling.base.Attributes import Attributes
from client.util.html.tooling.base.HTMLElement import HTMLElement


class ListItemElement(HTMLElement):
    def __init__(self, child_data=''):
        super().__init__('li')
        if isinstance(child_data, HTMLElement):
            self.append_child(child_data)
        else:
            self.set_inner_text(child_data)
