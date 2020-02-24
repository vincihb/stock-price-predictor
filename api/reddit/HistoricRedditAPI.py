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

    def set_start_epoch(self, start_date=dt.datetime(2020, 1, 1)):
        self._start = int(start_date.timestamp())

    def set_end_date(self, end_date=dt.datetime(2020, 1, 1)):
        self._end = int(end_date.timestamp())

    def set_query(self, query):
        self._query = query

    def search_posts(self):
        posts = self.api.search_submissions(after=self._start,
                                            subreddit=self._subreddit,
                                            filter=['url', 'author', 'title', 'subreddit', 'body', 'selftext'],
                                            limit=self._limit)
        return list(posts)

    def search_comments(self):
        comments = self.api.search_comments(after=self._start,
                                            subreddit=self._subreddit,
                                            filter=['url', 'author', 'title', 'subreddit', 'body', 'selftext'],
                                            limit=self._limit)
        return list(comments)

    def get_something(self):
        posts = self.api.search_submissions(after=self._start,
                                            subreddit=self._subreddit,
                                            sort="asc",
                                            filter=['author', 'title', 'subreddit', 'body', 'selftext', 'created_utc'],
                                            limit=self._limit)
        return list(posts)

