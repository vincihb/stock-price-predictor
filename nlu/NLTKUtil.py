from nltk.corpus import stopwords
from collections import Counter
from string import punctuation


class NLTKUtil:
    @staticmethod
    def get_bag_of_words(corpus):
        stop_words = list(punctuation) + stopwords.words('english')
        bow = []
        for w in corpus.split():
            # if the last character is punctuation, split it off
            if w[len(w) - 1] in punctuation:
                w = w[:-1]

            if w not in stop_words:
                bow.append(w)

        return bow

    @staticmethod
    def get_counted_bag_of_words(corpus, return_type='dict'):
        bow = NLTKUtil.get_bag_of_words(corpus)
        if return_type == 'dict':
            return dict(Counter(bow))
        else:
            return Counter(bow)

    @staticmethod
    def get_weighted_count(title, body, weight=5):
        title_bow = NLTKUtil.get_counted_bag_of_words(title)
        body_bow = NLTKUtil.get_counted_bag_of_words(body)
        for key in title_bow:
            if key in body_bow:
                body_bow[key] += weight * title_bow[key]
            else:
                body_bow[key] = weight * title_bow[key]

        body_bow = NLTKUtil.sort_bow(body_bow)
        return body_bow

    @staticmethod
    def get_weighted_stock_count(title, body, weight=5, suspect_ticker_weight=2):
        bow = NLTKUtil.get_weighted_count(title, body, weight)
        for key in bow:
            if 1 < len(key) < 5:
                bow[key] = bow[key] * suspect_ticker_weight

        return bow

    @staticmethod
    def sort_bow(dictionary):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}
