from client.util.charts.BarChart import BarChart
from client.util.charts.PieChart import PieChart
from client.util.charts.ScatterChart import ScatterChart


class ChartBuilder:
    def __init__(self, chart_type='bar', title='', data_set=None):
        self._type = chart_type
        self._title = title
        self._data_set = data_set
        self.chart = None

    def get_chart(self):
        if self._type == 'bar':
            self.chart = BarChart(title=self._title, data_set=self._data_set)
        elif self._type == 'pie':
            self.chart = PieChart(title=self._title, data_set=self._data_set)
        elif self._type == 'scatter':
            self.chart = ScatterChart(title=self._title, data_set=self._data_set)

        return self.chart.compile()
