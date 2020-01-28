from client.util.HTMLUtil import HTMLUtil

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
    def __init__(self, chart_type='bar', title='', data_set=None):
        if data_set is None:
            data_set = {'x': [{'label': 'no data', 'data': []}], 'y': []}

        self._raw_data_set = data_set
        self._xs = data_set['x']
        try:
            self._y = data_set['y']
        except KeyError:
            self._y = self.get_dummy_y(len(self._xs[0]['data']))

        self._type = chart_type
        self._title = title

        self._id = title.replace(' ', '_', 100)

        self._compiled_html = ''
        self._compiled_script = ''
        self._data_string = ''
        self._base_html = HTMLUtil.wrap_in_tag('', 'canvas', indent=1, attributes={ 'id': self._id })

        self._color_index = -1

    def build_script(self):
        self.get_options()

        self._compiled_script = SCRIPT_TEMPLATE.replace(TITLE_FORMAT, self._title)\
                                                     .replace(TYPE_FORMAT, self._type)\
                                                     .replace(LABEL_FORMAT, str(list(self._y)))\
                                                     .replace(ID_FORMAT, self._id)\
                                                     .replace(DATA_FORMAT, self._data_string)\
                                                     .replace(OPTIONS_FORMAT, self.resolve_options(self.get_options()))

    def compile(self):
        self.compile_data()
        self.build_script()
        self._compiled_html = self._base_html + HTMLUtil.get_indent(1) + self._compiled_script
        return self._compiled_html

    def get_next_color(self):
        self._color_index += 1
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'grey']
        return 'window.chartColors.' + colors[self._color_index % 7]

    def get_data_set_template(self):
        return DATA_SET_TEMPLATE

    # Child classes should override this function to determine how data is converted to be presented to Chart.js in JS
    def compile_data(self):
        self._data_string = ''
        for data in self._xs:
            color = ''
            try:
                color = data['color']
            except KeyError:
                color = self.get_next_color()

            self._data_string += self.get_data_set_template().replace(TITLE_FORMAT, data['label'])\
                                                             .replace(DATA_FORMAT, str(data['data']))\
                                                             .replace(COLOR_PATTERN, color, 2)

        self._data_string = self._data_string[:-1]

    @staticmethod
    def get_dummy_y(data_length):
        return range(0, data_length)

    def get_options(self):
        return {}

    @staticmethod
    def resolve_options(opts):
        options_str = ''
        for key in opts:
            options_str += '"' + key + '": ' + BaseChart.resolve_value(opts[key]) + ',\n\t\t\t'

        return options_str

    @staticmethod
    def resolve_value(val):
        if val is True:
            return 'true'
        elif val is False:
            return 'false'
        else:
            return str(val)

    def __str__(self):
        return self.compile()
