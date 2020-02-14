from nlu.NLTKUtil import NLTKUtil


class NLUSubjectTickerEstimator:
    @staticmethod
    def estimate(title, text):
        sorted_bow = NLTKUtil.get_weighted_stock_count(title, text)
        return NLTKUtil.get_likely_subject_stock(sorted_bow)