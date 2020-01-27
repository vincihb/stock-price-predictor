from datetime import date
from os import path
from client.util.TableBuilder import TableBuilder
from client.util.ListBuilder import ListBuilder


class Reporter:
    def __init__(self):
        self.date = str(date.today())
        self.title = 'Report: ' + self.date
        self.body = '<p>Empty Report</p>'

        self._local_dir = path.dirname(path.abspath(__file__))
        self._template_path = path.join(self._local_dir, 'template', 'root.html')
        self._compiled_path = path.join(self._local_dir, 'compiled')

        with open(self._template_path) as template_file:
            self.template = template_file.read()

    def set_title(self, title):
        self.title = title + ': ' + self.date

    def set_body(self, body):
        self.body = body

    def compile(self):
        with open(path.join(self._compiled_path, self.title + '.html'), 'w+') as compiled_file:
            compiled_file.write(self._compile_template())

    def _compile_template(self):
        return self.template.replace('$$__TITLE__$$', self.title, 2)\
                            .replace('$$__BODY__$$', str(self.body))\
                            .replace('$$__HEAD__$$', '')


values = [
    [1, 2, 3],
    [2, 3, 4],
    [3, 4, 5],
]

r = Reporter()
r.set_title('Wall Street Bets scan 2')
# r.set_body(TableBuilder(['Sample Header 1', 'Sample Header 2', 'Sample Header 3'], values).compile())
r.set_body(ListBuilder(['Sample LI 1', 'Sample LI 2', 'Sample LI 3'], list_header='Hello!'))
r.compile()
