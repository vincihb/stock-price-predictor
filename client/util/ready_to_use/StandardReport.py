from client.util.html.tooling.Header1Element import Header1Element
from client.util.html.tooling.LinkElement import LinkElement
from client.util.html.tooling.base.HTMLDocument import HTMLDocument
from client.util.html.tooling.base.document.HeadLinkElement import HeadLinkElement
from client.util.html.tooling.base.document.MetaElement import MetaElement
from client.util.html.tooling.base.document.ScriptElement import ScriptElement


class StandardReport(HTMLDocument):
    def __init__(self, doc_title=''):
        super().__init__(doc_title)

        self.get_default_meta()
        self.get_default_styles()
        self.get_default_scripts()

        self.body.append_child(LinkElement('Home', '../'))
        self.body.append_child(Header1Element(doc_title))

    def get_default_meta(self):
        meta = MetaElement()
        meta.set_attribute('charset', 'utf-8')
        self.head.append_child(meta)
        meta = MetaElement()
        meta.set_attribute('name', 'viewport')
        meta.set_attribute('content', 'width=device-width, initial-scale=1.0, viewport-fit=cover')
        self.head.append_child(meta)

    def get_default_styles(self):
        self.head.append_child(HeadLinkElement('stylesheet', '../css/bootstrap_v4_0_0.css'))
        self.head.append_child(HeadLinkElement('stylesheet', '../css/root.css'))

    def get_default_scripts(self):
        self.head.append_child(ScriptElement('../js/chart_js_2_9_3.js'))
        self.head.append_child(ScriptElement('../js/chart-colors.js'))


print(StandardReport('Test').render())
