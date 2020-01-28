from client.util.charts.BaseChart import BaseChart

'''
    Data Structure for line charts:
    {
        x: [
            { dataset_label: '', data: [], color: 'optional!|hex|color' }
            ...
        ],
        y: ['equal', 'number', 'of', 'labels', 'to', 'x', ...] | optional! we can shim this if needed
        start_date: datetime | optional, if your data is related to dates
        date_type: 'year', 'month', 'week', 'day' | optional
    }
'''

DATA_SET_TEMPLATE = '''{
                label: '$$__TITLE__$$',
                backgroundColor: $$__COLOR__$$,
                borderColor: $$__COLOR__$$,
                data: $$__DATA__$$,
                fill: false
            },'''


class LineChart(BaseChart):
    def __init__(self, title='', data_set=None):
        BaseChart.__init__(self, chart_type='line', title=title, data_set=data_set)

    def get_options(self):
        return {
            'fill': False
        }

    def get_data_set_template(self):
        return DATA_SET_TEMPLATE


SCRIPT = '''
var config = {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: window.chartColors.red,
            borderColor: window.chartColors.red,
            data: [10, 30, 39, 20, 25, 34, -10],
            fill: false,
        }, {
            label: 'My Second dataset',
            fill: false,
            backgroundColor: window.chartColors.blue,
            borderColor: window.chartColors.blue,
            data: [18, 33, 22, 19, 11, 39, 30],
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Min and Max Settings'
        },
        scales: {
            yAxes: [{
                ticks: {
                    // the data minimum used for determining the ticks is Math.min(dataMin, suggestedMin)
                    suggestedMin: 10,

                    // the data maximum used for determining the ticks is Math.max(dataMax, suggestedMax)
                    suggestedMax: 50
                }
            }]
        }
    }
};

window.onload = function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
};
'''