from client.util.HTMLUtil import HTMLUtil
from client.util.charts.BaseChart import BaseChart

TITLE_FORMAT = '$$__TITLE__$$'
DATA_FORMAT = '$$__DATA__$$'
COLOR_FORMAT = '$$__COLOR__$$'
DATA_SET_TEMPLATE = '''{
                                label: '$$__TITLE__$$',
                                backgroundColor: $$__COLOR__$$,
                                borderColor: '#fff',
                                data: $$__DATA__$$
                            },'''


class PieChart(BaseChart):
    def __init__(self, title, data_set):
        BaseChart.__init__(self, chart_type='pie', title=title, data_set=data_set)

    def compile_data(self):
        self._data_string = ''
        for data in self._ys:
            if 'color' in data:
                color = data['color']
            else:
                color = str([self.get_next_color() for _ in range(0, len(data['data']))]).replace("'", "", 100)

            self._data_string += HTMLUtil.get_indent(7) + DATA_SET_TEMPLATE.replace(TITLE_FORMAT, data['label']) \
                                                                           .replace(DATA_FORMAT, str(data['data'])) \
                                                                           .replace(COLOR_FORMAT, str(color))
