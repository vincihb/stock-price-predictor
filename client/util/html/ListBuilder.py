from client.util.html.tooling.Header2Element import Header2Element
from client.util.html.tooling.list.OrderedListElement import OrderedListElement
from client.util.html.tooling.list.UnorderedListElement import UnorderedListElement

BASE_INDENT = 3


class ListBuilder:
    UNORDERED = 'unordered'
    ORDERED = 'ordered'

    def __init__(self, list_items=None, list_type='unordered', list_header=''):
        if list_items is None:
            list_items = []

        self._header = None
        if list_header != '':
            self._header = Header2Element(list_header)

        if list_type == self.UNORDERED:
            self._list = UnorderedListElement()
        else:
            self._list = OrderedListElement()

        for item in list_items:
            self._list.add_item(item)

        self._list_header = list_header

    def compile(self):
        compiled = ''
        if self._header is not None:
            compiled = self._header.render()

        compiled += self._list.render()
        return compiled

    def __str__(self):
        return self.compile()
