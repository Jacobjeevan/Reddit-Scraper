from .Data import Data


class CommentData(Data):

    def __init__(self):
        super().__init__()
        self.length = 0
        self.comment = None
        self.clearData()

    def clearData(self):
        self.data = {"comment_body": [], "ups": [], "downs": [], "comment_ids": [],
                     "author_ids": [], "created_utc": [], "edited": [], "thread_ids": []}

    def retrieveData(self, comment, threadid):
        self.comment = comment
        if (super().IfAlreadyCollected(comment.id)):
            return 0
        else:
            self.retrieve(threadid)
            return 1

    def retrieve(self, threadid):
        commentID = self.comment.id
        self.length += 1
        self.data["thread_ids"].append(threadid)
        super().addToTracker(commentID)
        self.data["comment_ids"].append(commentID)
        self.data["comment_body"].append(self.comment.body)
        self.data["ups"].append(self.comment.ups)
        self.data["downs"].append(self.comment.downs)
        self.data["author_ids"].append(self.comment.author_fullname[3:])
        self.data["created_utc"].append(self.comment.created_utc)
        self.data["edited"].append(self.comment.edited)

    def saveData(self):
        super().saveData("CommentData.json")
        self.clearData()

    def loadData(self):
        self.data = super().loadData("CommentData.json")
