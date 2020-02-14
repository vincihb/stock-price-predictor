from datetime import datetime


class RedditResponseParser:
    @staticmethod
    def parse_submissions_to_dict(submissions, raw=False):
        if raw is True:
            return RedditResponseParser.parse_to_array(submissions)

        submission_dict = {
            "title": [],
            "score": [],
            "id": [],
            "url": [],
            "comms_num": [],
            "created": [],
            "body": []
        }

        for submission in submissions:
            submission_dict["title"].append(submission.title)
            submission_dict["score"].append(submission.score)
            submission_dict["id"].append(submission.id)
            submission_dict["url"].append(submission.permalink)
            submission_dict["num_comments"].append(submission.num_comments)
            submission_dict["created"].append(submission.created)
            submission_dict["body"].append(submission.selftext)

        return submission_dict

    @staticmethod
    def parse_to_array(submissions):
        subs = []
        for submission in submissions:
            subs.append({
                    "title": submission.title,
                    "score": submission.score,
                    "id": submission.id,
                    "url": submission.permalink,
                    "num_comments": submission.num_comments,
                    "created": submission.created_utc,
                    "body": submission.selftext
                })

        return subs

    @staticmethod
    def parse_to_date_batch(submissions):
        submissions = RedditResponseParser.parse_to_array(submissions)
        submissions.sort(key=lambda it: it['created'], reverse=True)

        date_epochs = {}
        current_epoch = []
        last_date = RedditResponseParser._get_date_from_unix(submissions[0]['created'])
        for sub in submissions:
            sub_date = RedditResponseParser._get_date_from_unix(sub['created'])
            if last_date is None or sub_date != last_date:
                if len(current_epoch) > 0:
                    date_epochs[last_date] = current_epoch

                current_epoch = []

            last_date = sub_date
            current_epoch.append(sub)

        date_epochs[last_date] = current_epoch
        return date_epochs

    @staticmethod
    def _get_date_from_unix(date):
        return str(datetime.fromtimestamp(int(date)).date())
