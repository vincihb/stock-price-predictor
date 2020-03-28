from client.util.html.tooling.base.document.HeadElement import HTMLHeadElement
from client.util.html.tooling.base.document.BodyElement import HTMLBodyElement
from client.util.html.tooling.base.document.TitleElement import TitleElement

ROOT_DOCUMENT_MARKUP = \
    '''
<!DOCTYPE html>
<html dir="ltr" lang="en-US">
    %%_HEAD_%%
    %%_BODY_%%
</html>
'''


class HTMLDocument:
    def __init__(self, title):
        self._children = []
        self._scripts = []
        self._styles = []
        self.title = []
        self._rendered_markup = ''

        self.head = HTMLHeadElement()
        self.head.append_child(TitleElement(title))
        self.body = HTMLBodyElement()

    def render(self):
        if self._rendered_markup != '':
            return self._rendered_markup

        self._rendered_markup = ROOT_DOCUMENT_MARKUP.replace('%%_HEAD_%%', self.head.render())\
                                                    .replace('%%_BODY_%%', self.body.render())

        return self._rendered_markup
