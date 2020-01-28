from client.util.HTMLUtil import HTMLUtil

BASE_INDENT = 3


class ListBuilder:
    UNORDERED = 'unordered'
    ORDERED = 'ordered'

    def __init__(self, list_items=None, list_type='unordered', list_header=''):
        if list_items is None:
            list_items = []

        self._list_items = list_items
        self._list_header = list_header
        self._list_type = list_type
        self._compiled_html = ''

    def compile(self):
        if self._list_header != '':
            self._compiled_html = HTMLUtil.wrap_in_tag(self._list_header, 'h2', BASE_INDENT)

        if self._list_type == ListBuilder.ORDERED:
            self._compiled_html += HTMLUtil.get_indent(BASE_INDENT) + '<ol>'
        else:
            self._compiled_html += HTMLUtil.get_indent(BASE_INDENT) + '<ul>'

        for item in self._list_items:
            self._compiled_html += HTMLUtil.wrap_in_tag(item, 'li', BASE_INDENT + 1)

        if self._list_type == ListBuilder.ORDERED:
            self._compiled_html += HTMLUtil.get_indent(BASE_INDENT) + '</ol>'
        else:
            self._compiled_html += HTMLUtil.get_indent(BASE_INDENT) + '</ul>'

        return self._compiled_html

    def __str__(self):
        return self.compile()
