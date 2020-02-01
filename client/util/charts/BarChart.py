from client.util.charts.BaseChart import BaseChart


class BarChart(BaseChart):
    def __init__(self, title='', data_set=None):
        BaseChart.__init__(self, chart_type='bar', title=title, data_set=data_set)

    def get_options(self):
        return {
            'scales': '''NOESC:{
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function (value) { if (Number.isInteger(value)) { return value; } },
                        stepSize: 1
                    }
                }]
            }\n'''
        }
