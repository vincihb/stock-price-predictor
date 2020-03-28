from client.util.HTMLUtil import HTMLUtil
from client.util.html.tooling.ButtonElement import ButtonElement


class ButtonBuilder:
    def __init__(self, text='', button_id='', attrs=None):
        if attrs is None:
            attrs = {}

        self._button = ButtonElement(text=text, button_id=button_id)
        for attr in attrs:
            self._button.set_attribute(attr, attrs[attr])

        self._compiled_html = ''

    def compile(self):
        return self._button.render()

    def __str__(self):
        return self.compile()
