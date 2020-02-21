from collections import Counter
from os import path
from nlu.NLTKUtil import NLTKUtil


def read_sentiment_file_to_array(f_name):
    local_path = path.dirname(path.abspath(__file__))
    path_to_list = path.join(local_path, '..', 'data', 'jargon', f_name)
    with open(path_to_list) as file_data:
        word_list = [line.strip() for line in file_data]

    return word_list


NEGATIVE_WORDS = read_sentiment_file_to_array('negative.txt')
POSITIVE_WORDS = read_sentiment_file_to_array('positive.txt')


class SentimentAnalyzer:
    @staticmethod
    def get_net_sentiment(discussion):
        positive_sent = 0
        negative_sent = 0

        counted = SentimentAnalyzer.get_counter_for_dd(discussion)
        norm_factor = sum(counted.values(), 0.0)
        for key in counted:
            if key in POSITIVE_WORDS:
                positive_sent += counted[key] / norm_factor

            if key in NEGATIVE_WORDS:
                negative_sent += counted[key] / norm_factor

        sentiment_ratio = positive_sent / negative_sent

        return positive_sent, negative_sent, sentiment_ratio

    @staticmethod
    def get_counter_for_dd(daily_discussion):
        counter = Counter()
        tickers = daily_discussion['tickers']
        for t in tickers:
            if t == 'misc':
                subs = tickers[t]
            else:
                subs = tickers[t]['submissions']

            for sub in subs:
                if 'body' not in sub:
                    continue

                counter.update(NLTKUtil.get_bag_of_words(sub['body'].lower(), length_filter=2))

        return counter
