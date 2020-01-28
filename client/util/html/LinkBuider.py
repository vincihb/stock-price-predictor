from client.util.HTMLUtil import HTMLUtil


class LinkBuilder:
    def __init__(self, text='', url=''):
        self._text = text
        self._url = url
        self._compiled_html = ''

    def compile(self):
        self._compiled_html = HTMLUtil.wrap_in_tag(self._text, 'a', one_line=True, attributes={'href': self._url})
        return self._compiled_html

    def __str__(self):
        return self.compile()
