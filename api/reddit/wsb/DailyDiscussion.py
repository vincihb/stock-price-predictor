from api.reddit.RedditAPI import RedditAPI
from api.util.Pickler import Pickler
from nlu.NLUSubjectTickerEstimator import NLUSubjectTickerEstimator
from os import path, listdir
from praw.models import MoreComments
from datetime import date


class DailyDiscussion:
    def __init__(self):
        self._wsb = RedditAPI().get_subreddit(sub_name='wallstreetbets')
        self._local_dir = path.dirname(path.abspath(__file__))
        self._cache_path = path.join(self._local_dir, 'cache')

    def get_daily_discussion(self, for_date=None, strict_match=False):
        if for_date is not None and isinstance(for_date, date):
            for_date = for_date.toordinal()

        # if we're passed a date, search to see if we have a match for the date already
        if for_date is not None:
            data = self._get_daily_discussion_meta(for_date, strict_match=strict_match)
            if len(data) != 0:
                return data

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
            post_meta = self._get_post_meta(post)
            self._dump_to_cache(post_meta, post_file_name)

    def _get_post_meta(self, post):
        post_meta = {
            "title": post.title,
            "link": post.permalink,
            "id": post.id,
            'date': int(post.created)
        }

        tickers = {
            "misc": []
        }

        comments = self.resolve_all_comments(post.comments)
        for comment in comments:
            if isinstance(comment, MoreComments):
                continue

            body = comment.body

            ticker = NLUSubjectTickerEstimator.estimate('', body)
            print(body, ticker)
            if ticker is None:
                tickers['misc'].append(self._serialize_comment(comment))
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
        return post_meta

    def _get_daily_discussion_meta(self, for_date, strict_match=False):
        if isinstance(for_date, date):
            for_date = for_date.toordinal()

        found_dd = self._is_in_cache(for_date, strict_match=strict_match)
        return [self.get_from_cache(dd) for dd in found_dd]

    def _is_in_cache(self, for_date, strict_match=False, _from_fuzz=False):
        if isinstance(for_date, date):
            for_date = for_date.toordinal()

        # read out the files in the cache
        files = [f for f in listdir(self._cache_path) if path.isfile(path.join(self._cache_path, f)) and f != "README.md"]
        # return an array of the files where its timestamp matches the date you're searching for
        found = [dd for dd in files if date.fromtimestamp(int(dd.split('-')[0])).toordinal() == for_date]
        if len(found) == 0 and not _from_fuzz and not strict_match:
            return self.fuzz_for_dd(for_date)

        return found

    # If we don't find data, recursively walking back in time to find some
    def fuzz_for_dd(self, for_date, _current_depth=0, _max_depth=5):
        last_date = for_date - 1
        dd = self._is_in_cache(last_date, _from_fuzz=True)
        if len(dd) == 0 and _current_depth < _max_depth:
            return self.fuzz_for_dd(last_date, _current_depth + 1)

        return dd

    @staticmethod
    def resolve_all_comments(post_comments):
        comments = list(post_comments)
        while isinstance(comments[-1], MoreComments):
            print('Getting more comments...')
            more_comments = list(comments[-1].comments())
            comments = comments[:-1] + more_comments

        return comments

    @staticmethod
    def _serialize_comment(comment):
        return {
            'link': comment.permalink,
            'body': comment.body,
            'score': comment.score,
            'created': int(comment.created)
        }

    def _check_cache(self, post_id):
        return self.get_from_cache(post_id + ".pickle")

    def get_from_cache(self, filename):
        return Pickler.load_obj(path.join(self._cache_path, filename))

    def _dump_to_cache(self, obj, post_id):
        print('Dumping results to pickle file: ' + post_id + '.pickle')
        Pickler.save_obj(obj, path.join(self._cache_path, post_id + ".pickle"))
