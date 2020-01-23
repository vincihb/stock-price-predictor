from datetime import date


class Reporter:
    def __init__(self):
        self.date = str(date.today())

    def produce_report(self):
        with open('./template/root.html') as root_template_file:
            html_template = root_template_file.read()
            html_template.replace('$$__REPORT_DATE__$$', self.date)
