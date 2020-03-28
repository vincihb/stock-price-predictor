from client.util.html.tooling.base.Attributes import Attributes
from client.util.html.tooling.base.HTMLElement import HTMLElement


class ButtonElement(HTMLElement):
    def __init__(self, text='', button_id='', button_class='primary'):
        super().__init__('button')

        self.set_inner_text(text)
        self.set_attribute(Attributes.ID, button_id)
        self.add_class('btn')
        self.add_class('btn-' + button_class)
        self.add_class('gen-report')
