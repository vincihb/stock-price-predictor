from api import reddit as RedditAPI

r = RedditAPI.RedditAPI()
print(r.get_new('wallstreetbets'))
