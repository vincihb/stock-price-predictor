""" Simple compilation of all of the ticker files from the raw """
alpha = 'abcdefghijklmnopqrstuvwxyz'

base_dir = '../../data/tickers/raw/'
data_dirs = ['nasdaq', 'nyse', 'tsx']
etfs = base_dir + 'etfs/etfs.txt'
rh = base_dir + 'rh/rh_top_100.txt'

# concatenate all of the tickers into a single array
all_tickers = []
for data_dir in data_dirs:
    for char in alpha:
        with open(base_dir + data_dir + '/' + data_dir + '_' + char + '.txt') as current:
            for line in current:
                if '-' in line or '.' in line:
                    continue

                all_tickers.append(line)

# make all the tickers unique and sort them alphabetically
all_tickers = list(set(all_tickers))
all_tickers.sort()

# concat them back into a big string
ticker_text = ''
for ticker in all_tickers:
    ticker_text = ticker_text + ticker

# slice off the first new line
ticker_text = ticker_text[1:len(ticker_text)]

# and write it all back to a compilation file
with open('../../data/tickers/compiled/all_tickers.txt', 'w') as new_file:
    new_file.write(ticker_text)

print("Happy hunting!")
