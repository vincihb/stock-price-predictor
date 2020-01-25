"""MarketWatch scraper v3 -- classified!"""
from tool.scrapers.util.HTMLParser import HTMLParser
import os
from db.SqlExecutor import SqlExecutor
import time


class MarketWatchScraper:
    STOCK_URL_PATTERN = 'https://www.marketwatch.com/investing/stock/$$TICKER$$/profile'
    FUND_URL_PATTERN = 'https://www.marketwatch.com/investing/fund/$$TICKER$$'

    TICKER_PATTERN = '$$TICKER$$'
    DESCRIPTION_PATTERN = '$$DESC$$'

    def __init__(self):
        self.executor = SqlExecutor()

    @staticmethod
    def _curl_for_html(url):
        # slow down crawls to prevent lockout by marketwatch
        time.sleep(0.5)
        html_out = os.popen('curl -s "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (K HTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36" ' + url)
        return html_out.read()

    @staticmethod
    def _get_name(body, name_locator, ticker, resource_type):
        if '<div class="important">There were no matches found for ' in body:
            print("No data found at all for %s ticker %s, skipping..." % (resource_type, ticker))
            return False

        name = HTMLParser.grep_for(body, name_locator)
        if name == '':
            print("No name found for %s ticker %s, skipping..." % (resource_type, ticker))
            return False

        return name

    def update_stock_metadata(self, ticker):
        update_sql_template = \
            "UPDATE `COMPANY` SET NAME=?, DESCRIPTION=?, INDUSTRY=?, SECTOR=?, REVENUE=?, NET_INCOME=?, EMPLOYEES=?, " \
            "RESOURCE_URL=?, CLASS='STOCK' WHERE TICKER='$$TICKER$$';"

        resource_url = MarketWatchScraper.STOCK_URL_PATTERN.replace(MarketWatchScraper.TICKER_PATTERN, ticker)
        raw_html = MarketWatchScraper._curl_for_html(resource_url)

        name = MarketWatchScraper._get_name(raw_html, 'id="instrumentname"', ticker, 'stock')
        if not name:
            return False

        description = HTMLParser.grep_for(raw_html, 'div class="full"', 2)
        industry = HTMLParser.grep_for(raw_html, '>Industry<', 1)
        sector = HTMLParser.grep_for(raw_html, 'Sector', 1)
        employees = HTMLParser.grep_for(raw_html, 'Employees', 2)
        net_income = HTMLParser.grep_for(raw_html, 'Net Income', 1)
        revenue = HTMLParser.grep_for(raw_html, '>Revenue<', 1)

        sql = update_sql_template.replace(MarketWatchScraper.TICKER_PATTERN, ticker)
        self.executor.exec_insert(sql,
                                  (name, description, industry, sector, revenue, net_income, employees, resource_url))

        print('%s: %s - found and loaded!' % (ticker, name))
        return True

    def update_fund_metadata(self, ticker):
        update_sql_template = \
            "UPDATE `COMPANY` SET NAME=?, DESCRIPTION=?, RESOURCE_URL=?, CLASS='FUND' WHERE TICKER='$$TICKER$$';"

        resource_url = MarketWatchScraper.FUND_URL_PATTERN.replace(MarketWatchScraper.TICKER_PATTERN, ticker)
        raw_html = MarketWatchScraper._curl_for_html(resource_url)

        name = MarketWatchScraper._get_name(raw_html, 'class="company__name"', ticker, 'fund')
        if not name:
            return False

        description = HTMLParser.grep_for(raw_html, 'class="description__text"', 2)

        sql = update_sql_template.replace(MarketWatchScraper.TICKER_PATTERN, ticker)
        self.executor.exec_insert(sql, (name, description, resource_url))

        print('%s: %s - found and loaded!' % (ticker, name))

    def update_all_tickers(self):
        rows = self.executor.exec_select('SELECT * FROM COMPANY WHERE NAME IS NULL')
        all_rows = rows.fetchall()
        for row in all_rows:
            success = self.update_stock_metadata(row[0])
            if not success:
                self.update_fund_metadata(row[0])

