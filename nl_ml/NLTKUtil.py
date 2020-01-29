from nltk.corpus import stopwords
from collections import Counter
from string import punctuation


class NLTKUtil:
    @staticmethod
    def get_bag_of_words(corpus):
        stop_words = list(punctuation) + stopwords.words('english')
        bow = []
        for w in corpus.lower().split():
            # don't carry single letters into the BOW
            if w not in stop_words and len(w) > 1:
                bow.append(w)

        return bow

    @staticmethod
    def get_counted_bag_of_words(corpus):
        bow = NLTKUtil.get_bag_of_words(corpus)
        return Counter(bow)

corpus = 'Hello my name is hello and that\'s not cool you know hey hello'
print(NLTKUtil.get_bag_of_words(corpus))