from client.util.charts.BaseChart import BaseChart


class ScatterChart(BaseChart):
    def __init__(self, title='', data_set=None, x_label='', y_label=''):
        BaseChart.__init__(self, chart_type='scatter', title=title, data_set=data_set, x_label=x_label, y_label=y_label)

    def get_options(self):
        return {
            'scales': '''NOESC:{
                            xAxes: [
                                {
                                    gridLines: { color: "#444", zeroLineColor: '#888' },
                                    scaleLabel: {
                                        display: true,
                                        labelString: '$$__X_AXIS_NAME__$$',
                                        fontColor:'#888',
                                        fontSize: 10
                                    }
                                }
                            ],
                            yAxes: [
                                {
                                    gridLines: { color: "#444", zeroLineColor: '#888' },
                                    scaleLabel: {
                                        display: true,
                                        labelString: '$$__Y_AXIS_NAME__$$',
                                        fontColor:'#888',
                                        fontSize: 10
                                    }
                                }]
                        }'''.replace('$$__X_AXIS_NAME__$$', self._x_label)
                            .replace('$$__Y_AXIS_NAME__$$', self._y_label),
            'tooltips': '''NOESC:{
                                    callbacks: {
                                        mode: 'x',
                                        label: function(tooltipItem, myData) {
                                            var label = myData.datasets[tooltipItem.datasetIndex].label || '';
                                            if (label)
                                                label += ': ';

                                            label += parseFloat(tooltipItem.value).toFixed(2);
                                            return label;
                                        }
                                    }
                                }'''
        }