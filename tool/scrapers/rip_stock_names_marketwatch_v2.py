"""Marketwatch scraper v2 - uses """

from tool.scrapers.util.HTMLParser import HTMLParser
import os
from db.SqlExecutor import SqlExecutor

URL_PATTERN = 'https://www.marketwatch.com/investing/stock/$$TICKER$$/profile'
'https://www.marketwatch.com/investing/stock/acb/profile'

TICKER_PATTERN = '$$TICKER$$'
DESCRIPTION_PATTERN = '$$DESC$$'

UPDATE_SQL = \
    "UPDATE `COMPANY` SET NAME=?, DESCRIPTION=?, INDUSTRY=?, SECTOR=?, REVENUE=?, NET_INCOME=?, EMPLOYEES=?, " \
    "RESOURCE_URL=? WHERE TICKER='$$TICKER$$';"


def update_ticker_metadata(ticker):
    executor = SqlExecutor(debug=True)
    resource_url = URL_PATTERN.replace(TICKER_PATTERN, ticker)
    html_out = os.popen('curl -s ' + resource_url)
    raw_html = html_out.read()

    if '<div class="important">There were no matches found for ' in raw_html:
        print("No data found for ticker %s, skipping..." % ticker)
        return

    name = HTMLParser.grep_for(raw_html, 'id="instrumentname"')
    if name == '':
        print("No data found for ticker %s, skipping..." % ticker)
        return

    description = HTMLParser.grep_for(raw_html, 'div class="full"', 2)
    industry = HTMLParser.grep_for(raw_html, '>Industry<', 1)
    sector = HTMLParser.grep_for(raw_html, 'Sector', 1)
    employees = HTMLParser.grep_for(raw_html, 'Employees', 2)
    net_income = HTMLParser.grep_for(raw_html, 'Net Income', 1)
    revenue = HTMLParser.grep_for(raw_html, '>Revenue<', 1)

    sql = UPDATE_SQL.replace(TICKER_PATTERN, ticker)
    executor.exec_insert(sql, (name, description, industry, sector, revenue, net_income, employees, resource_url))

    print('%s: %s - found and loaded!' % (ticker, name))


def update_all_tickers():
    outer_executor = SqlExecutor(debug=True)
    rows = outer_executor.exec_select('SELECT * FROM COMPANY')
    for row in rows:
        update_ticker_metadata(row[0])