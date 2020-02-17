from api.reddit.RedditAPI import RedditAPI


class DailyDiscussion:
    def __init__(self):
        self._wsb = RedditAPI().get_subreddit(sub_name='wallstreetbets')

    def get_daily_discussion(self):
        results = self._wsb.search(query='flair:daily discussion', time_filter='all', sort="new")
        for post in results:
            print(post.title)


DailyDiscussion().get_daily_discussion()