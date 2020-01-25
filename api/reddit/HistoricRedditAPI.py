import psaw
import datetime as dt


class HistoricRedditAPI:
    def __init__(self):
        self.api = psaw.PushshiftAPI()
        self._subreddit = ''
        self._limit = 10
        self._start = int(dt.datetime(2020, 1, 1).timestamp())
        self._end = 0
        self._query = ''

    def set_subreddit(self, sub):
        self._subreddit = sub

    def set_limit(self, limit):
        self._limit = limit

    def set_start_epoch(self, start_date):
        self._start = start_date

    def set_end_date(self, end_date):
        self._end = end_date

    def set_query(self, query):
        self._query = query

    def search_top_level(self):
        request = self.api.search_submissions(after=self._start,
                                              subreddit=self._subreddit,
                                              filter=['url', 'author', 'title', 'subreddit', 'body', 'selftext'],
                                              limit=10)
        return list(request)

    def search_comments(self):
        list(self.api.search_comments(after=self._start,
                                         subreddit=self._subreddit,
                                         filter=['url', 'author', 'title', 'subreddit', 'body', 'selftext'],
                                         limit=10))

    def get_something(self):
        return list(self.api.search_submissions(after=self._start,
                                    subreddit=self._subreddit,
                                    filter=['author', 'title', 'subreddit', 'body', 'selftext'],
                                    limit=10))
