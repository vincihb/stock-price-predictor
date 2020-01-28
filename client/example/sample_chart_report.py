import datetime

from api.local_stocks.Ticker import Ticker
from client.util.ChartBuilder import ChartBuilder
from client.Reporter import Reporter

t = Ticker()
stocks = t.get_n_stocks(n=10)

count = 0
values = []
for stock in stocks:
    values.append({
        'label': '$' + stock[0],
        'data': [count, count + 5, count + 10, count + 5, count]
    })

    count += 1

data = {
    'ys': values
}

r = Reporter()
r.set_title('Sample Chart Report')
r.set_body(ChartBuilder(chart_type='line', title='Sample Line Chart', data_set=data))

bar_data = {'ys': data['ys'][:3]}
r.append_to_body(ChartBuilder(chart_type='bar', title='Sample Bar Chart', data_set=bar_data))

# Note that pie charts require x labels for its data, and can only accept one data set, otherwise weird things happen
pie_data = {
    'x': ['One', 'Two', 'Three', 'Four', 'Five'],
    'ys': data['ys'][2:3]
}
r.append_to_body(ChartBuilder(chart_type='pie', title='Sample Pie Chart', data_set=pie_data))

data['start_date'] = datetime.date.today()
r.append_to_body(ChartBuilder(chart_type='line', title='Chart with Generated X Datetimes', data_set=data))

r.compile()
