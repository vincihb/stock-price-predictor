from client.util.html.tooling.base.HTMLElement import HTMLElement
from client.util.html.tooling.ListItemElement import ListItemElement

# DO NOT INSTANTIATE DIRECTLY #
# Proto-class for ul and ol lists #


class ListElement(HTMLElement):
    def add_item(self, child_data):
        list_item = ListItemElement()
        if isinstance(child_data, HTMLElement):
            list_item.append_child(child_data)
        else:
            list_item.set_inner_text(child_data)

        self.append_child(list_item)


