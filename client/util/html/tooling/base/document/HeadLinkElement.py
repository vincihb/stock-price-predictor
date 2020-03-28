from client.util.html.tooling.base.HTMLElement import HTMLElement


class HeadLinkElement(HTMLElement):
    def __init__(self, rel, href):
        super().__init__('link')
        self.set_attribute('rel', rel)
        self.set_attribute('href', href)
