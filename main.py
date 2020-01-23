import reddit.RedditAPI as RedditAPI

r = RedditAPI.RedditAPI()
print(r.get_new('wallstreetbets'))
