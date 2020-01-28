from client.util.charts.BarChart import BarChart
from client.util.charts.PieChart import PieChart
from client.util.charts.ScatterChart import ScatterChart
from client.util.charts.LineChart import LineChart

'''
    Data Set Structure for charts:
    {
        ys: [
            { dataset_label: '', data: [], color: 'optional!|hex|color' }
            ...
        ],
        x: ['equal', 'number', 'of', 'labels', 'to', 'x', ...] | optional! we shim this if needed
        start_date: datetime | optional, if your data is related to dates, we can auto-populate the x axis with dates
        date_type: 'year', 'month', 'week', 'day' | optional
    }
'''


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
        elif self._type == 'line':
            self.chart = LineChart(title=self._title, data_set=self._data_set)

        return self.chart.compile()

    def __str__(self):
        return self.get_chart()
