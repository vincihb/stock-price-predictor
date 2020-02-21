from api.reddit.wsb.DailyDiscussion import DailyDiscussion
from collections import Counter
from nlu.SentimentAnalyzer import SentimentAnalyzer

# Tweak this to remove words that you don't think are important
CUSTOM_TRIM_WORDS = [
    'today', 'day', 'tomorrow', 'time',
    'fucking', 'fuck', 'really',
    'it\'s', 'it’s', 'right', 'make', 'know', 'lol',
    'time', 'one', '[deleted', 'i\'m', 'gonna', 'would', 'i’m',
    'stock', 'see', 'people', 'last', 'still', 'next', 'anyone',
    'going'
]


def get_top_n_words_in_last_m_discussions(n=100, m=10):
    dd = DailyDiscussion().get_n(n=m)
    c = Counter()
    for d in dd:
        tickers = d['tickers']
        d_counter = SentimentAnalyzer.get_counter_for_dd(d)
        c.update(d_counter)


    print("Top %d Words Found:")
    for word in c.most_common(n):
        print(word)


get_top_n_words_in_last_m_discussions(100, 30)
