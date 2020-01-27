BASE_INDENT = 3


class TableBuilder:
    def __init__(self, headers=None, rows=None):
        if rows is None:
            rows = [[]]

        if headers is None:
            headers = []

        self._compiled_html = ''
        self._headers = headers
        self._rows = rows

    def compile(self):
        self._compiled_html = '<table>'

        t_head = '\n\t<thead>\n\t\t<tr>'
        for header in self._headers:
            t_head = t_head + '\n\t\t\t<th>' + str(header) + '</th>'

        t_head = t_head + '\n\t\t</tr>\n\t</thead>'

        t_body = '\n\t<tbody>'
        for row in self._rows:
            t_body = t_body + '\n\t\t<tr>'
            for column in row:
                t_body = t_body + '\n\t\t\t<td>' + str(column) + '</td>'

            t_body = t_body + '\n\t\t</tr>'

        t_body = t_body + '\n\t</tbody>'

        self._compiled_html = self._compiled_html + t_head + t_body + '\n\t</table>'

        return self._compiled_html

    def __str__(self):
        return self.compile()
