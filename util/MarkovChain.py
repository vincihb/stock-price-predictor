import numpy as np
from api.alpha_vantage.HistoricAlphaVantageAPI import HistoricAlphaVantageAPI


class MarkovChain:
    def __init__(self, ticker):
        self.ticker = ticker

    def build_markov_chain(self):
        historic_data = HistoricAlphaVantageAPI()
        ticker_data = historic_data.get_all_data(self.ticker)
        print(ticker_data[0])
        print(ticker_data[len(ticker_data) - 1])
        pass


if __name__ == "__main__":
    mc = MarkovChain('TSLA')
    mc.build_markov_chain()
