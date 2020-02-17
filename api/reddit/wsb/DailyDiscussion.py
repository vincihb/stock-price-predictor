from api.reddit.RedditAPI import RedditAPI
from api.util.Pickler import Pickler
from nlu.NLUSubjectTickerEstimator import NLUSubjectTickerEstimator
from os import path


class DailyDiscussion:
    def __init__(self):
        self._wsb = RedditAPI().get_subreddit(sub_name='wallstreetbets')
        self._local_dir = path.dirname(path.abspath(__file__))
        self._cache_path = path.join(self._local_dir, 'cache')

    def get_daily_discussion(self):
        results = self._wsb.search(query='flair:daily discussion', time_filter='all', sort="new")
        first = True
        for post in results:
            # skip the first post, as it will always be incomplete
            if first is True:
                first = False
                continue

            post_file_name = str(int(post.created)) + '-' + post.id

            if self._check_cache(post_file_name) is not None:
                print('Already cached results for post with ID: ' + post.id)
                continue

            # set up the collections
            post_meta = {
                "title": post.title,
                "link": post.permalink,
                "id": post.id,
                'date': int(post.created)
            }

            tickers = {
                "misc": []
            }

            post.comments.replace_more(limit=None)
            for comment in post.comments:
                body = comment.body

                ticker = NLUSubjectTickerEstimator.estimate('', body)
                print(body, ticker)
                if ticker is None:
                    tickers['misc'].append(body)
                elif ticker in tickers:
                    tickers[ticker]['count'] += 1
                    tickers[ticker]['submissions'].append(self._serialize_comment(comment))
                else:
                    tickers[ticker] = {
                        'count': 1,
                        'submissions': [self._serialize_comment(comment)],
                        'description': ticker[2]
                    }

            post_meta['tickers'] = tickers
            self._dump_to_cache(post_meta, post_file_name)

    @staticmethod
    def _serialize_comment(comment):
        return {
            'link': comment.permalink,
            'body': comment.body,
            'score': comment.score,
            'created': int(comment.created)
        }


    def _check_cache(self, post_id):
        return Pickler.load_obj(path.join(self._cache_path, post_id + ".pickle"))

    def _dump_to_cache(self, obj, post_id):
        print('Dumping results to pickle file: ' + post_id + '.pickle')
        Pickler.save_obj(obj, path.join(self._cache_path, post_id + ".pickle"))


DailyDiscussion().get_daily_discussion()
