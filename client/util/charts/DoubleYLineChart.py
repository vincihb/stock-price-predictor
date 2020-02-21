from client.util.charts.BaseChart import BaseChart
from client.util.HTMLUtil import HTMLUtil

COLOR_PATTERN = '$$__COLOR__$$'
TITLE_FORMAT = '$$__TITLE__$$'
DATA_FORMAT = '$$__DATA__$$'
Y_AX_ID = "$$__Y_AX_ID__$$"
DATA_SET_TEMPLATE = '''{
                                label: '$$__TITLE__$$',
                                backgroundColor: $$__COLOR__$$,
                                borderColor: $$__COLOR__$$,
                                data: $$__DATA__$$,
                                fill: false,
                                pointRadius: 0,
                                lineTension: 0,
                                borderWidth: 2,
                                yAxisID: $$__Y_AX_ID__$$
                            },'''


class DoubleYLineChart(BaseChart):
    def __init__(self, title='', data_set=None, x_label='', y_label=''):
        BaseChart.__init__(self, chart_type='line', title=title, data_set=data_set, x_label=x_label, y_label=y_label)
        self._secondary_y_label = self._raw_data_set['y2_label'] if self._raw_data_set['y2_label'] is not None else ''

    def get_data_set_template(self):
        return DATA_SET_TEMPLATE

    def compile_data(self):
        self._data_string = ''
        for data in self._raw_data_set['ys']:
            color = self.resolve_data_color(data)
            self._data_string += HTMLUtil.get_indent(7) + self.get_data_set_template()\
                                                              .replace(TITLE_FORMAT, data['label'])\
                                                              .replace(DATA_FORMAT, str(data['data']))\
                                                              .replace(COLOR_PATTERN, color, 2)\
                                                              .replace(Y_AX_ID, "'A'")

        for data in self._raw_data_set['secondary_ys']:
            color = self.resolve_data_color(data)
            self._data_string += HTMLUtil.get_indent(7) + self.get_data_set_template() \
                                                              .replace(TITLE_FORMAT, data['label']) \
                                                              .replace(DATA_FORMAT, str(data['data'])) \
                                                              .replace(COLOR_PATTERN, color, 2) \
                                                              .replace(Y_AX_ID, "'B'")

        self._data_string = self._data_string[:-1]

    def get_options(self):
        return {
            'scales': '''NOESC:{
                                    xAxes: [
                                        {
                                            gridLines: { color: "#444", zeroLineColor: '#888' },
                                            scaleLabel: {
                                                display: true,
                                                labelString: '$$__X_AXIS_NAME__$$',
                                                fontColor:'#888',
                                                fontSize: 10
                                            }
                                        }
                                    ],
                                    yAxes: [
                                        {
                                            gridLines: { color: "#444", zeroLineColor: '#888' },
                                            scaleLabel: {
                                                display: true,
                                                labelString: '$$__Y_AXIS_NAME__$$',
                                                fontColor:'#888',
                                                fontSize: 10
                                            },
                                            id: 'A',
                                            type: 'linear',
                                            position: 'left'
                                        },
                                        {
                                            gridLines: { color: "#444", zeroLineColor: '#888' },
                                            scaleLabel: {
                                                display: true,
                                                labelString: '$$__Y_AXIS_NAME_2__$$',
                                                fontColor:'#888',
                                                fontSize: 10
                                            },
                                            id: 'B',
                                            type: 'linear',
                                            position: 'right'
                                        }]
                                }'''.replace('$$__X_AXIS_NAME__$$', self._x_label)
                                    .replace('$$__Y_AXIS_NAME__$$', self._y_label)
                                    .replace('$$__Y_AXIS_NAME_2__$$', self._secondary_y_label),
        }
