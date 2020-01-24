import sqlite3

class Company:
    # NAME=?, DESCRIPTION=?, INDUSTRY=?, SECTOR=?, REVENUE=?, NET_INCOME=?, EMPLOYEES=?
    def __init__(self, ticker, name, description, industry, sector, revenue, net_income, employees):
        self.ticker = ticker
        self.name = name
        self.description = description
        self.industry = industry
        self.sector = sector
        self.revenue = revenue
        self.net_income = net_income
        self.employees = employees

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%f;%f" % (self.ticker, self.name, self.description)