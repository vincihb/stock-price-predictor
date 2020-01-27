from client.util.charts.BaseChart import BaseChart

'''
    data_set = [
        { title: string, data: [*] }
    ]
'''


class BarChart(BaseChart):
    def __init__(self, title='', data_set=None):
        BaseChart.__init__(self, chart_type='bar', title=title, data_set=data_set)

        if data_set is None:
            data_set = []

        self._data_set = data_set

    def compile_data(self):
        pass
