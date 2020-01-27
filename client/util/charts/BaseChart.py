from client.util.HTMLUtil import HTMLUtil

TYPE_FORMAT = '$$__TYPE__$$'
LABEL_FORMAT = '$$__LABELS__$$'
ID_FORMAT = '$$__ID__$$'
TITLE_FORMAT = '$$__TITLE__$$'
DATA_FORMAT = '$$__DATA__$$'
SCRIPT_TEMPLATE = '''
var ctx = document.getElementById('$$__ID__$$').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: '$$__TYPE__$$',

    // The data for our dataset
    data: {
        labels: [$$__LABELS__$$],
        datasets: [{
            label: '$$__TITLE__$$',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: $$__DATA__$$
        }]
    },

    options: {}
});
'''


class BaseChart:
    def __init__(self, chart_type='bar', title='', data_set=None):
        if data_set is None:
            data_set = []

        self._type = chart_type
        self._title = title
        self._data_set = data_set

        self._id = title.replace(' ', '_', 100)

        self._compiled_script = ''
        self._data_string = ''
        self._base_html = HTMLUtil.wrap_in_tag('', 'canvas', indent=1, attributes={ id: self._id })

        self._color_index = 0

    def build_script(self):
        self._compiled_script = self._compiled_script.replace(TITLE_FORMAT, self._title)\
                                                     .replace(TYPE_FORMAT, self._type)\
                                                     .replace(LABEL_FORMAT, self._type)\
                                                     .replace(ID_FORMAT, self._id)\
                                                     .replace(DATA_FORMAT, self._data_string)

    def compile(self):
        self.compile_data()
        self.build_script()
        return self._base_html + HTMLUtil.get_indent(1) + self._compiled_script

    def get_next_color(self):
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'grey']
        return 'window.chartColors.' + colors[self._color_index % 7]

    # Child classes should override this function to determine how data is converted to be presented to Chart.js in JS
    def compile_data(self):
        raise Exception('compile_data must be overridden by child classes')

    @staticmethod
    def get_dummy_y(data_length):
        return range(0, data_length)
