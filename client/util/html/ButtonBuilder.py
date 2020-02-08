from client.util.HTMLUtil import HTMLUtil


class ButtonBuilder:
    def __init__(self, text='', button_id='', attrs=None):
        if attrs is None:
            attrs = {}

        self._text = text
        self._attrs = attrs
        self._attrs['id'] = button_id
        self._attrs['class'] = 'btn btn-primary gen-report'
        self._compiled_html = ''

    def compile(self):
        self._compiled_html = HTMLUtil.wrap_in_tag(self._text, 'button', one_line=True, attributes=self._attrs)
        return self._compiled_html

    def __str__(self):
        return self.compile()
