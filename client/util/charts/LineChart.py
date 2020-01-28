from client.util.charts.BaseChart import BaseChart

DATA_SET_TEMPLATE = '''{
                label: '$$__TITLE__$$',
                backgroundColor: $$__COLOR__$$,
                borderColor: $$__COLOR__$$,
                data: $$__DATA__$$,
                fill: false
            },'''


class LineChart(BaseChart):
    def __init__(self, title='', data_set=None):
        BaseChart.__init__(self, chart_type='line', title=title, data_set=data_set)

    def get_options(self):
        return {
            'fill': False
        }

    def get_data_set_template(self):
        return DATA_SET_TEMPLATE
