from client.util.HTMLUtil import HTMLUtil


class ScrollableDiv:
    def __init__(self, body, max_height, indent=5, min_width='10rem'):
        self._body = body
        self._height = max_height
        self._min_width = min_width
        self._indent = indent
        self._compiled_html = ''

    def compile(self):
        attrs = {
            'style': "max-height: " + self._height + "; overflow: auto; min-width: " + self._min_width + ";"
        }

        self._compiled_html = HTMLUtil.wrap_in_tag(self._body, 'div', self._indent, attributes=attrs)
        return self._compiled_html
