from client.util.html.tooling.LinkElement import LinkElement


class LinkBuilder:
    def __init__(self, text='', url=''):
        self._link = LinkElement(text, url, target='_blank')

    def compile(self):
        return self._link.render()

    def __str__(self):
        return self.compile()
