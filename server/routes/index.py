from os import listdir, path
from client.util.HTMLUtil import HTMLUtil
from client.util.html.ButtonBuilder import ButtonBuilder
from client.util.html.ListBuilder import ListBuilder
from client.util.html.LinkBuider import LinkBuilder

valid_report_types = ['NLU', 'NLU_Timing', 'Refresh_DD', 'Markov_Chain']


def index_routes(app):
    _local_dir = path.dirname(path.abspath(__file__))
    client_path = path.join(_local_dir, '..', '..', 'client')

    @app.route('/')
    def index():
        report_path = path.join(client_path, 'compiled')

        # read out and sort all compiled reports (ignore the README)
        files = [f for f in listdir(report_path) if path.isfile(path.join(report_path, f)) and f != "README.md"]
        files.sort()

        file_links = [LinkBuilder(text=f.replace('.html', ''), url='/report?name=' + f) for f in files]
        file_list = ListBuilder(list_items=file_links, list_header='Your Reports')

        buttons = [ButtonBuilder(text='New ' + b + ' Report', button_id=b, attrs={"data-type": b}) for b in valid_report_types]
        button_list = ListBuilder(list_items=buttons, list_header=' Generate Reports')

        template = HTMLUtil.get_template('index.html')\
            .replace('$$__REPORTS__$$', file_list.compile())\
            .replace('$$__GEN_REPORTS__$$', button_list.compile())

        return template

