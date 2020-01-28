from api.local_stocks.Ticker import Ticker
from client.util.ChartBuilder import ChartBuilder
from client.Reporter import Reporter

t = Ticker()
stocks = t.get_n_stocks(n=10)
values = [

]

count = 0
for stock in stocks:
    values.append({
        'label': stock[0],
        'data': [count, count + 5, count + 10, count + 5, count]
    })

    count += 1

data = {
    'x': values
}

r = Reporter()
r.set_title('Sample Chart Report')
r.set_body(ChartBuilder(chart_type='line', title='Sample Report', data_set=data))
r.compile()
