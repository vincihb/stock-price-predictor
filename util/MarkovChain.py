import numpy as np
from api.alpha_vantage.HistoricAlphaVantageAPI import HistoricAlphaVantageAPI


def trim(x, y):
    min_y_index = find_min(y)
    max_y_index = find_max(y)
    print(min_y_index)
    print(max_y_index)
    if min_y_index == 0:
        min_y_index = 1
    if max_y_index == x.size - 1:
        max_y_index = x.size - 2
    if min_y_index is None or max_y_index is None:
        return None, None
    x, y = remove_zeros(x[min_y_index - 1: max_y_index + 2], y[min_y_index - 1: max_y_index + 2])
    return x, y


# TODO: Check if array is size zero
def remove_zeros(x, y):
    x_array = [x[0]]
    y_array = [y[0]]
    for index in range(1, y.size - 1):
        if y[index] > 0:
            x_array.append(x[index])
            y_array.append(y[index])
    x_array.append(x[x.size - 1])
    y_array.append(y[y.size - 1])
    return np.array(x_array), np.array(y_array)


def find_min(array):
    print("Array Size is: ")
    print(array.size)
    print("#######")
    for index in range(array.size):
        if array[index] > 0:
            return index

    return None


def find_max(array):
    for index in range(array.size - 1, 0, -1):
        if array[index] > 0:
            return index

    return None


class MarkovChain:
    def __init__(self, ticker):
        self.ticker = ticker
        self.historic_data = HistoricAlphaVantageAPI()
        self.ticker_data = self.historic_data.get_all_data(self.ticker)
        self._build_historic_percentage_data()

    @staticmethod
    def expected_value(x, y):
        mu = 0
        for index in range(x.size):
            mu += x[index] * y[index]
        return mu

    @staticmethod
    def var(x, y):
        mu = MarkovChain.expected_value(x, y)
        sigma = 0
        for index in range(x.size):
            sigma += x[index] * x[index] * y[index]
        return sigma - mu * mu

    def build_markov_chain(self):
        largest_gain, largest_loss = self._biggest_one_day_gain_loss()
        average_gain, average_loss = self._average_one_day_fluctuation()
        self._build_raw_markov_chain(average_gain, average_loss, largest_gain, largest_loss)
        previous_day_percentage = 0.00
        for percentage in self.historic_percentage_data:
            percentage = round(percentage, 2)
            previous_day_index = self._linear_index_map(previous_day_percentage)
            percentage_index = self._linear_index_map(percentage)
            self.markov_chain[previous_day_index, percentage_index] = \
                self.markov_chain[previous_day_index, percentage_index] + 1
            previous_day_percentage = percentage
        self._normalize()
        return self.markov_chain

    def _predict_past_percentage(self, past_percentage):
        row_index = self._linear_index_map(past_percentage)
        x = []
        for index in range(len(self.markov_chain[row_index, :])):
            x.append(self._linear_percentage_map(index))
        print("Predict a " + str(self.markov_chain[row_index, :]) + "% change in stock value")
        return trim(np.array(x), self.markov_chain[row_index, :])

    def predict(self):
        latest_percentage = self.historic_percentage_data[len(self.historic_percentage_data) - 2]
        x, y = self._predict_past_percentage(latest_percentage)
        return x, y

    def _normalize(self):
        for row_index in range(self.markov_chain.shape[0]):
            total_sum = np.sum(self.markov_chain[row_index, :])
            if total_sum != 0:
                self.markov_chain[row_index, :] = self.markov_chain[row_index, :]/total_sum
        pass

    def _build_raw_markov_chain(self, average_gain, average_loss, largest_gain, largest_loss):
        self.step_size = round(max(average_gain, abs(average_loss)) / 10, 1)
        if self.step_size == 0.0:
            self.step_size = 0.1
        self.max_range = round(max(largest_gain, abs(largest_loss)), 0)
        self.size_of_matrix = int(self.max_range / self.step_size) * 2
        self.markov_chain = np.zeros(shape=[self.size_of_matrix, self.size_of_matrix], dtype='float32')
        return self.markov_chain

    def _linear_index_map(self, percentage):
        index = round((self.size_of_matrix/(2*self.max_range)) * percentage + self.size_of_matrix/2)
        if index > self.size_of_matrix - 1:
            index = self.size_of_matrix - 1
        elif index < 0:
            index = 0
        return int(index)

    def _linear_percentage_map(self, index):
        percentage = (self.max_range*2)/self.size_of_matrix * index - self.max_range
        return round(percentage, 2)

    def _build_historic_percentage_data(self):
        self.historic_percentage_data = []
        previous_close = float(self.ticker_data[0]['close'])
        indicator = 0
        for item in self.ticker_data:
            open_price = float(item['open'])
            # Store after hour trading data
            # if indicator != 0:
                # self.historic_percentage_data.append((open_price - previous_close) / previous_close * 100)
            indicator = 1
            close_price = float(item['close'])
            self.historic_percentage_data.append((close_price - open_price) / open_price * 100)
            previous_close = close_price
        return self.historic_percentage_data

    def _biggest_one_day_gain_loss(self):
        return max(self.historic_percentage_data), min(self.historic_percentage_data)

    def _smallest_one_day_gain_loss(self):
        temp_array = []
        for item in self.historic_percentage_data:
            if item != 0.0:
                temp_array.append(abs(item))
        return min(temp_array)

    def _average_one_day_fluctuation(self):
        overall_positive_percentage_change = 0
        overall_negative_percentage_change = 0
        for percentage in self.historic_percentage_data:
            if percentage > 0:
                overall_positive_percentage_change += percentage
            else:
                overall_negative_percentage_change += percentage
        return overall_positive_percentage_change / len(self.historic_percentage_data), \
               overall_negative_percentage_change / len(self.historic_percentage_data)


if __name__ == "__main__":
    mc = MarkovChain('TSLA')
    markov_chain = mc.build_markov_chain()
    mc.predict()
    print("Hello")

