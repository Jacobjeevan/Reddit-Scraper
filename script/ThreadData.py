from Data import Data
import praw


class ThreadData(Data):

    def __init__(self):
        super().__init__()
        self.length = 0
        self.clearData()

    def clearData(self):
        self.data = {"thread_ids": [], "title": [], "author_ids": [], "upvotes": [
        ], "gildings": [], "created_utc": [], "premium": [], "num_comments": [], "edited": []}

    def retrieveData(self, submission):
        numComments = submission.num_comments
        submissionID = submission.id
        if (submissionID in super().getTracker()):
            pass
        else:
            self.length += 1
            self.retrieveThreadAuthor(submission)
            self.data["thread_ids"].append(submissionID)
            super().addToTracker(submissionID)
            self.data["title"].append(submission.title)
            self.data["upvotes"].append(submission.ups)
            self.data["edited"].append(submission.edited)
            self.data["gildings"].append(submission.gildings)
            self.data["created_utc"].append(submission.created_utc)
            self.data["num_comments"].append(numComments)

    def retrieveThreadAuthor(self, submission):
        try:
            self.data["author_ids"].append(submission.author_fullname[3:])
            self.data["premium"].append(submission.author_premium)
        except praw.exceptions.RedditAPIException:
            self.data["author_ids"].append("NaN")
            self.data["premium"].append("NaN")

    def saveData(self):
        super().saveData("ThreadData.json")
        self.clearData()

    def loadData(self):
        self.data = super().loadData("ThreadData.json")
