from client.util.charts.BaseChart import BaseChart

DATA_SET_TEMPLATE = '''{
                                label: '$$__TITLE__$$',
                                backgroundColor: $$__COLOR__$$,
                                borderColor: $$__COLOR__$$,
                                data: $$__DATA__$$,
                                fill: false,
                                pointRadius: 0,
                                lineTension: 0,
                                borderWidth: 2
                            },'''


class LineChart(BaseChart):
    def __init__(self, title='', data_set=None, x_label='', y_label=''):
        BaseChart.__init__(self, chart_type='line', title=title, data_set=data_set, x_label=x_label, y_label=y_label)

    def get_options(self):
        return {
            'fill': False,
            'tooltips': '''NOESC:{
                            intersect: false,
                            mode: 'index',
                            callbacks: {
                                label: function(tooltipItem, myData) {
                                    var label = myData.datasets[tooltipItem.datasetIndex].label || '';
                                    if (label)
                                        label += ': ';
                                    
                                    label += parseFloat(tooltipItem.value).toFixed(2);
                                    return label;
                                }
                            }
                        }''',
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
                        }'''
                        .replace('$$__X_AXIS_NAME__$$', self._x_label)
                        .replace('$$__Y_AXIS_NAME__$$', self._y_label)
            }

    def get_data_set_template(self):
        return DATA_SET_TEMPLATE
