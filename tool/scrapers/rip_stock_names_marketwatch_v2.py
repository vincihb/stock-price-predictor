"""Marketwatch scraper v2 - uses """

from tool.scrapers.util.HTMLParser import HTMLParser
import os
from db.SqlExecutor import SqlExecutor

URL_PATTERN = 'https://www.marketwatch.com/investing/stock/$$TICKER$$/profile'
FUND_URL_PATTERN = 'https://www.marketwatch.com/investing/fund/$$TICKER$$'

TICKER_PATTERN = '$$TICKER$$'
DESCRIPTION_PATTERN = '$$DESC$$'


def split_too_long_tickers():
    e = SqlExecutor(debug=True)
    rows = e.exec_select('SELECT * FROM COMPANY WHERE NAME is NULL')
    for row in rows:
        # if the ticker is too long,
        if len(row[0]) > 4:
            ticker = row[0]
            # print(ticker)
            results = ticker.rsplit(ticker[0])
            results = results[1:]
            for result in results:
                if result is not '':
                    new_name = ticker[0] + result
                    e.exec_insert("INSERT INTO `COMPANY` (`NAME`) VALUES (?)", (new_name,))
                    print(ticker[0] + result)


def update_ticker_metadata(ticker):
    update_sql_template = \
        "UPDATE `COMPANY` SET NAME=?, DESCRIPTION=?, INDUSTRY=?, SECTOR=?, REVENUE=?, NET_INCOME=?, EMPLOYEES=?, " \
        "RESOURCE_URL=? WHERE TICKER='$$TICKER$$';"

    resource_url = URL_PATTERN.replace(TICKER_PATTERN, ticker)
    html_out = os.popen('curl -s ' + resource_url)
    raw_html = html_out.read()

    if '<div class="important">There were no matches found for ' in raw_html:
        print("No data found for ticker %s, skipping..." % ticker)
        return False

    name = HTMLParser.grep_for(raw_html, 'id="instrumentname"')
    if name == '':
        print("No data found for ticker %s, skipping..." % ticker)
        return False

    description = HTMLParser.grep_for(raw_html, 'div class="full"', 2)
    industry = HTMLParser.grep_for(raw_html, '>Industry<', 1)
    sector = HTMLParser.grep_for(raw_html, 'Sector', 1)
    employees = HTMLParser.grep_for(raw_html, 'Employees', 2)
    net_income = HTMLParser.grep_for(raw_html, 'Net Income', 1)
    revenue = HTMLParser.grep_for(raw_html, '>Revenue<', 1)

    executor = SqlExecutor(debug=True)
    sql = update_sql_template.replace(TICKER_PATTERN, ticker)
    executor.exec_insert(sql, (name, description, industry, sector, revenue, net_income, employees, resource_url))

    print('%s: %s - found and loaded!' % (ticker, name))
    executor.close()
    return True


def update_fund_metadata(ticker):
    update_sql_template = \
        "UPDATE `COMPANY` SET NAME=?, DESCRIPTION=?, RESOURCE_URL=?, CLASS='FUND' WHERE TICKER='$$TICKER$$';"

    resource_url = FUND_URL_PATTERN.replace(TICKER_PATTERN, ticker)
    html_out = os.popen('curl -s ' + resource_url)
    raw_html = html_out.read()

    if '<div class="important">There were no matches found for ' in raw_html:
        print("No data found for ticker %s, skipping..." % ticker)
        return

    name = HTMLParser.grep_for(raw_html, 'class="company__name"')
    if name == '':
        print("No data found for ticker %s, skipping..." % ticker)
        return

    description = HTMLParser.grep_for(raw_html, 'class="description__text"', 2)

    executor = SqlExecutor(debug=True)
    sql = update_sql_template.replace(TICKER_PATTERN, ticker)
    executor.exec_insert(sql, (name, description, resource_url))
    executor.close()

    print('%s: %s - found and loaded!' % (ticker, name))


def update_all_tickers():
    outer_executor = SqlExecutor(debug=True)
    rows = outer_executor.exec_select('SELECT * FROM COMPANY WHERE NAME IS NULL')
    all_rows = rows.fetchall()
    outer_executor.close()
    for row in all_rows:
        success = update_ticker_metadata(row[0])
        if not success:
            update_fund_metadata(row[0])


update_all_tickers()
