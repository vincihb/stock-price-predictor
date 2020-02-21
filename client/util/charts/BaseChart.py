from client.util.HTMLUtil import HTMLUtil
from client.util.charts.DataSet import DataSet

TYPE_FORMAT = '$$__TYPE__$$'
LABEL_FORMAT = '$$__LABELS__$$'
ID_FORMAT = '$$__ID__$$'
TITLE_FORMAT = '$$__TITLE__$$'
DATA_FORMAT = '$$__DATA__$$'
OPTIONS_FORMAT = '$$__OPTIONS__$$'
SCRIPT_TEMPLATE = '''
            <script>
                var ctx = document.getElementById('$$__ID__$$').getContext('2d');
                var chart = new Chart(ctx, {
                    // The type of chart we want to create
                    type: '$$__TYPE__$$',
                
                    // The data for our dataset
                    data: {
                        labels: $$__LABELS__$$,
                        datasets: [
                            $$__DATA__$$
                        ]
                    },
                
                    options: {
                        title: {
                            display: true,
                            text: '$$__TITLE__$$'
                        },
                        $$__OPTIONS__$$
                    }
                });
            </script>
'''

COLOR_PATTERN = '$$__COLOR__$$'
DATA_SET_TEMPLATE = '''{
                                label: '$$__TITLE__$$',
                                backgroundColor: $$__COLOR__$$,
                                borderColor: $$__COLOR__$$,
                                data: $$__DATA__$$
                            },'''


class BaseChart:
    def __init__(self, chart_type='bar', title='', data_set=None, x_label='', y_label=''):
        if data_set is None:
            data_set = DataSet()
            data_set.set_x([])
            data_set.set_ys([{'label': 'no data', 'data': []}])
        elif isinstance(data_set, dict):
            data_set = DataSet(from_data=data_set)

        self._raw_data_set = data_set.get_data_dict()
        self._ys = self._raw_data_set['ys']

        self._x = self._raw_data_set['x']

        self._type = chart_type
        self._title = title

        self._id = title.replace(' ', '_', 100)

        self._compiled_html = ''
        self._compiled_script = ''
        self._data_string = ''
        self._base_html = HTMLUtil.wrap_in_tag('', 'canvas', indent=3, attributes={'id': self._id})

        self._color_index = -1

        self._x_label = x_label
        self._y_label = y_label

    def compile(self):
        self.compile_data()
        self.build_script()
        self._compiled_html = HTMLUtil.get_indent(1) + self._base_html + HTMLUtil.get_indent(1) + self._compiled_script
        return self._compiled_html

    def compile_data(self):
        self._data_string = ''
        for data in self._ys:
            color = self.resolve_data_color(data)
            self._data_string += HTMLUtil.get_indent(7) + self.get_data_set_template()\
                                                              .replace(TITLE_FORMAT, data['label'])\
                                                              .replace(DATA_FORMAT, str(data['data']))\
                                                              .replace(COLOR_PATTERN, color, 2)

        self._data_string = self._data_string[:-1]

    def get_next_color(self):
        self._color_index += 1
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'grey']
        return 'window.chartColors.' + colors[self._color_index % 7]

    def build_script(self):
        self.get_options()
        self._compiled_script = SCRIPT_TEMPLATE.replace(TITLE_FORMAT, self._title, 2)\
                                               .replace(TYPE_FORMAT, self._type)\
                                               .replace(LABEL_FORMAT, str(list(self._x)))\
                                               .replace(ID_FORMAT, self._id)\
                                               .replace(DATA_FORMAT, self._data_string)\
                                               .replace(OPTIONS_FORMAT, self.resolve_options(self.get_options()))

    # Child classes should override this method to provide custom options for chart.js
    def get_options(self):
        return {}

    # Child classes should override this method to provide custom data set templates for chart.js
    def get_data_set_template(self):
        return DATA_SET_TEMPLATE

    def resolve_data_color(self, data):
        if 'color' in data:
            color = data['color']
        else:
            color = self.get_next_color()

        return color

    @staticmethod
    def resolve_options(opts):
        options_str = ''
        for key in opts:
            options_str += '"' + key + '": ' + BaseChart.resolve_value(opts[key]) + ',' + HTMLUtil.get_indent(6)

        return options_str

    @staticmethod
    def resolve_value(val):
        if val is True:
            return 'true'
        elif val is False:
            return 'false'
        elif 'NOESC:' in val:
            return val.replace('NOESC:', '')
        else:
            return str(val)

    def __str__(self):
        return self.compile()
