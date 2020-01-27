from client.util.charts.BaseChart import BaseChart


class PieChart(BaseChart):
    def __init__(self, title, data_set):
        BaseChart.__init__(self, chart_type='pie', title=title, data_set=data_set)

    def compile_data(self):
        pass
