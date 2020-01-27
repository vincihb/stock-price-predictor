from db.SqlExecutor import SqlExecutor


class Ticker:
    @staticmethod
    def get_ticker(ticker):
        executor = SqlExecutor()
        result = executor.exec_select('SELECT * FROM COMPANY WHERE TICKER=?', (ticker,))
        return result.fetchone()

    @staticmethod
    def get_stock(ticker):
        return Ticker.get_ticker_with_class(ticker, 'STOCK')

    @staticmethod
    def get_etf(ticker):
        return Ticker.get_ticker_with_class(ticker, 'FUND')

    @staticmethod
    def get_ticker_with_class(ticker, fd_class):
        executor = SqlExecutor()
        result = executor.exec_select('SELECT * FROM COMPANY WHERE TICKER=? AND CLASS=?', (ticker, fd_class))
        return result.fetchone()

    @staticmethod
    def get_n_stocks(n=5):
        executor = SqlExecutor()
        result = executor.exec_select('SELECT * FROM COMPANY WHERE CLASS=? AND NAME IS NOT NULL LIMIT ?', ('STOCK', n))
        return result.fetchall()
