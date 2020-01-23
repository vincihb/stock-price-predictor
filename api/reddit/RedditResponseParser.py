

class RedditResponseParser:
    @staticmethod
    def parse_submissions_to_dict(submissions):
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
            submission_dict["url"].append(submission.url)
            submission_dict["comms_num"].append(submission.num_comments)
            submission_dict["created"].append(submission.created)
            submission_dict["body"].append(submission.selftext)

        return submission_dict