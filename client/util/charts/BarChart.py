from client.util.charts.BaseChart import BaseChart


class BarChart(BaseChart):
    def __init__(self, title='', data_set=None, x_label='', y_label=''):
        BaseChart.__init__(self, chart_type='bar', title=title, data_set=data_set, x_label=x_label, y_label=y_label)

    def get_options(self):
        return {
            'scales': '''NOESC:{
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function (value) { if (Number.isInteger(value)) { return value; } },
                        stepSize: 1
                    },
                    scaleLabel: {
                        display: true,
                        labelString: '$$__Y_AXIS_NAME__$$',
                        fontColor:'#888',
                        fontSize: 10
                    }
                }]
            }\n'''.replace('$$__Y_AXIS_NAME__$$', self._y_label)
        }
