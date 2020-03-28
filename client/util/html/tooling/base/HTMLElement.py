from client.util.HTMLUtil import HTMLUtil
from client.util.html.tooling.base.Attributes import Attributes


class HTMLElement:
    def __init__(self, node_type):
        self._node_type = node_type
        self._attrs = dict()
        self._text = ''
        self._children = []
        self._class_list = []

    def set_attribute(self, attr_name, value):
        self._attrs[attr_name] = value

    def get_attribute(self, attr_name):
        return self._attrs.get(attr_name)

    def set_inner_text(self, text):
        self._text = text

    def add_class(self, class_name):
        self._class_list.append(class_name)

    def remove_class(self, class_name):
        return self._class_list.remove(class_name)

    def has_class(self, class_name):
        return class_name in self._class_list

    def get_text(self):
        return self._text

    def append_child(self, child):
        self._children.append(child)

    def remove_child(self, child):
        return self._children.remove(child)

    def query_selector(self, selector):
        result = selector in self._children
        return None

    def query_selector_all(self, selector):
        result = selector in self._children
        return None

    def get_element_by_id(self, element_id):
        return self.query_selector('#' + element_id)

    def get_element_by_class_name(self, class_name):
        return self.query_selector('.' + class_name)

    def get_element_by_tag_name(self, tag_name):
        return self.query_selector(tag_name)

    def render(self, indent=1):
        self._attrs[Attributes.CLASS] = ' '.join(self._class_list)
        if len(self._children) == 0:
            return HTMLUtil.wrap_in_tag(self._text, self._node_type, indent, self._attrs, one_line=True)

        child_markup = ''
        for child in self._children:
            if isinstance(child, HTMLElement):
                child_markup += child.render(indent=indent + 1)
            else:
                child_markup += str(child)

        return HTMLUtil.wrap_in_tag(child_markup, self._node_type, indent, self._attrs, one_line=False)
