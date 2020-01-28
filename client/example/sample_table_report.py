from api.local_stocks.Ticker import Ticker
from client.util.html.TableBuilder import TableBuilder
from client.Reporter import Reporter

t = Ticker()
acb = t.get_stock('ACB')
hexo = t.get_stock('HEXO')
tlry = t.get_stock('TLRY')
values = [
    acb[:3],
    hexo[:3],
    tlry[:3]
]

r = Reporter()
r.set_title('Sample Stock Report')
r.set_body(TableBuilder(['Ticker', 'Company Name', 'Description'], values).compile())
r.compile()
