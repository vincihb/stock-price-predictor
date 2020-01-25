from api.reddit.RedditAPI import RedditAPI
from api.reddit.HistoricRedditAPI import HistoricRedditAPI

r = HistoricRedditAPI()
r.set_subreddit('wallstreetbets')
data = r.get_something()
for el in data:
    print(el)
