import praw
from os import path
import json
from api.reddit.RedditResponseParser import RedditResponseParser


class RedditAPI:
    def __init__(self):
        self._local_dir = path.dirname(path.abspath(__file__))
        self._config_path = path.join(self._local_dir, '..', '..', 'config', 'reddit_api.json')

        with open(self._config_path) as json_data:
            data = json.load(json_data)

        self.USER = data['username']
        self.PASSWORD = data['password']
        self.ID = data['id']
        self.SECRET = data['secret']

        self.reddit = self._init_reddit()

    def _init_reddit(self):
        return praw.Reddit(client_id=self.ID,
                           client_secret=self.SECRET,
                           user_agent='glowing-pancake-praw/hi.reddit',
                           username=self.USER,
                           password=self.PASSWORD)

    def get_new(self, sub_name, limit=100, cast_to='dict'):
        sub = self.get_subreddit(sub_name)
        submissions = sub.new(limit=limit)
        return self._pretty_format(submissions, cast_to)

    def get_hot(self, sub_name, limit=100, cast_to='dict'):
        sub = self.get_subreddit(sub_name)
        submissions = sub.hot(limit=limit)
        return self._pretty_format(submissions, cast_to)

    def get_subreddit(self, sub_name):
        return self.reddit.subreddit(sub_name)

    @staticmethod
    def _pretty_format(submissions, cast_to):
        if cast_to == 'dict':
            return RedditResponseParser.parse_submissions_to_dict(submissions)
        elif cast_to == 'array':
            return RedditResponseParser.parse_to_array(submissions)
        elif cast_to == 'epoch':
            return RedditResponseParser.parse_to_date_batch(submissions)
        else:
            return submissions
