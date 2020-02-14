class Sorting:
    @staticmethod
    def sort_by_score(item):
        return item['score']

    @staticmethod
    def sort_by_mentions(item):
        return item[1]
