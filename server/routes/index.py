from os import listdir, path
from client.util.HTMLUtil import HTMLUtil
from client.util.html.ListBuilder import ListBuilder
from client.util.html.LinkBuider import LinkBuilder


def index_routes(app):
    _local_dir = path.dirname(path.abspath(__file__))
    client_path = path.join(_local_dir, '..', '..', 'client')

    @app.route('/')
    def index():
        report_path = path.join(client_path, 'compiled')
        files = [f for f in listdir(report_path) if path.isfile(path.join(report_path, f))]
        file_links = [LinkBuilder(text=f.replace('.html', ''), url='/report?name=' + f) for f in files]
        file_list = ListBuilder(list_items=file_links, list_header="Your Reports")
        template = HTMLUtil.get_template('index.html').replace('$$__REPORTS__$$', file_list.compile())
        return template

