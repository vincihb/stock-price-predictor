from client.util.charts.BaseChart import BaseChart


class ScatterChart(BaseChart):
    def __init__(self, title='', data_set=None):
        BaseChart.__init__(self, chart_type='scatter', title=title, data_set=data_set)
