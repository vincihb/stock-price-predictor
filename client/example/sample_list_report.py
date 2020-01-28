from api.local_stocks.Ticker import Ticker
from client.util.html.ListBuilder import ListBuilder
from client.Reporter import Reporter

t = Ticker()
stocks = t.get_n_stocks(n=10)
values = []

for stock in stocks:
    values.append(stock[0] + ' - ' + stock[1])


r = Reporter()
r.set_title('Sample Stock List Report')
r.set_body(ListBuilder(values, list_header="Stock tickers").compile())
r.compile()
