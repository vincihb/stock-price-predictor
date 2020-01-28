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
    def __init__(self, title='', data_set=None):
        BaseChart.__init__(self, chart_type='line', title=title, data_set=data_set)

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
                        }'''
            }

    def get_data_set_template(self):
        return DATA_SET_TEMPLATE
