from datetime import date
from os import path

from client.util.HTMLUtil import HTMLUtil


class Reporter:
    def __init__(self):
        self.date = str(date.today())
        self.title = 'Report: ' + self.date
        self.summary = ''
        self.body = ''

        self._local_dir = path.dirname(path.abspath(__file__))
        self._template_path = path.join(self._local_dir, 'template', 'root.html')
        self._compiled_path = path.join(self._local_dir, 'compiled')

        with open(self._template_path) as template_file:
            self.template = template_file.read()

    def set_title(self, title):
        self.title = title + ': ' + self.date

    def set_body(self, body):
        self.body = HTMLUtil.wrap_in_tag(body, 'section', indent=2, one_line=False)

    def append_to_body(self, html):
        self.body += '\n\t\t<br />' + HTMLUtil.wrap_in_tag(html, 'section', indent=2, one_line=False)

    def set_summary(self, summary):
        self.summary = summary

    def compile(self):
        with open(path.join(self._compiled_path, self.title + '.html'), 'w+') as compiled_file:
            compiled_file.write(self._compile_template())

    def _compile_template(self):
        if self.body == '':
            self.body = '\n\t\t<section>\n\t\t\t<p>Empty Report</p>\n\t\t</section>'

        if self.summary != '':
            self.summary = HTMLUtil.wrap_in_tag(self.summary, 'p') + '\n'

        self.body = HTMLUtil.wrap_in_tag(self.body, 'main', indent=1, one_line=False)

        return self.template.replace('$$__TITLE__$$', self.title, 2)\
                            .replace('$$__BODY__$$', self.summary + str(self.body))\
                            .replace('$$__HEAD__$$', '')
