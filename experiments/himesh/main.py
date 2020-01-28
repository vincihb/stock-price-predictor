from api.local_stocks.Ticker import Ticker
from api.reddit.RedditAPI import RedditAPI
from api.reddit.HistoricRedditAPI import HistoricRedditAPI
print(Ticker.get_stock("HEXO"))
r = RedditAPI()
a = r.get_hot('stocks')
for submission in a['title']:
    print(submission)
print(r.get_hot('stocks'))
b = HistoricRedditAPI()
b.set_subreddit('wallstreetbets')
c = b.get_something()
for submission in c:
    print(submission.title)