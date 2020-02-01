from client.util.charts.BaseChart import BaseChart
from client.util.HTMLUtil import HTMLUtil

TITLE_FORMAT = '$$__TITLE__$$'
COLOR_PATTERN = '$$__COLOR__$$'
DATA_FORMAT = '$$__DATA__$$'
DATA_SET_TEMPLATE = '''{
                                label: '$$__TITLE__$$',
                                backgroundColor: $$__COLOR__$$,
                                borderColor: $$__COLOR__$$,
                                data: $$__DATA__$$
                            },'''


class HorizontalBarChart(BaseChart):
    def __init__(self, title='', data_set=None):
        BaseChart.__init__(self, chart_type='horizontalBar', title=title, data_set=data_set)

    def compile_data(self):
        self._data_string = ''
        for data in self._ys:
            color = []
            for data_item in data['data']:
                if '-' in data_item:
                    color.append('window.chartColors.red')
                else:
                    color.append('window.chartColors.green')

            self._data_string += HTMLUtil.get_indent(7) + self.get_data_set_template() \
                .replace(TITLE_FORMAT, data['label']) \
                .replace(DATA_FORMAT, str(data['data'])) \
                .replace(COLOR_PATTERN, str(color).replace("'", "", 1000), 2)

        self._data_string = self._data_string[:-1]

    def get_options(self):
        return {
            'fill': False,
            'elements': '''NOESC:{
                    rectangle: {
                        borderWidth: 2,
                    }
                }\n''',
            'responsive': True,
            'legend': '''NOESC:{
                    position: 'right',
                }\n'''
        }
