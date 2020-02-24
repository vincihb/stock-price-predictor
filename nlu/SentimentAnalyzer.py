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
    # Look at the range of post and return the score for all the tickers mentioned
    @staticmethod
    def get_net_sentiment_historic(range_of_posts):
        to_return = []
        for submission in range_of_posts:
            title = submission.title
            body = submission.selftext
            bag_of_words = NLTKUtil.get_weighted_stock_count(title, body)

            ticker = NLTKUtil.get_likely_subject_stock(bag_of_words)

            if ticker is not None:
                ticker_symbol = ticker[0]
            else:
                continue

            positive_match, negative_match = SentimentAnalyzer.get_positive_and_negative_matches(bag_of_words)
            score = positive_match - negative_match
            to_return.append((ticker_symbol, score))

        return to_return

    @staticmethod
    def get_positive_and_negative_matches(bag_of_words):
        positive_match = 0
        negative_match = 0
        for word in bag_of_words.keys():
            for positive_stem in POSITIVE_WORDS:
                if positive_stem in word.lower():
                    positive_match += bag_of_words[word]

            for negative_stem in NEGATIVE_WORDS:
                if negative_stem in word.lower():
                    negative_match += bag_of_words[word]
        return positive_match, negative_match

    @staticmethod
    def get_average_discussion_sentiment(dd_array):
        pos = 0
        neg = 0
        ratio = 0
        for d in dd_array:
            positive, negative, s_ratio = SentimentAnalyzer.get_net_sentiment(d)
            pos += positive
            neg += negative
            ratio += s_ratio

        # return the average sentiment for all of the discussions for the trading day
        n = len(dd_array)
        return pos / n, neg / n, ratio / n

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
