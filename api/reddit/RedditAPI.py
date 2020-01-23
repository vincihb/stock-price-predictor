import praw
import json
from api.reddit.RedditResponseParser import RedditResponseParser


class RedditAPI:
    def __init__(self):
        with open('config/reddit_api.json') as json_data:
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

    def get_new(self, sub_name, limit=100):
        sub = self.get_subreddit(sub_name)
        return RedditResponseParser.parse_submissions_to_dict(sub.new(limit=limit))

    def get_hot(self, sub_name, limit=100):
        sub = self.get_subreddit(sub_name)
        return RedditResponseParser.parse_submissions_to_dict(sub.hot(limit=limit))

    def get_subreddit(self, sub_name):
        return self.reddit.subreddit(sub_name)
