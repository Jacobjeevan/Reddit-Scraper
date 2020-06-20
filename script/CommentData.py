from Data import Data

class CommentData(Data):

    def __init__(self):
        super().__init__()
        self.data = {"comment_body": [], "ups": [], "downs": [], "comment_ids": [],
                     "author_ids": [], "created_utc": [], "edited": [], "thread_ids": []}

    def retrieveData(self, comment, threadid):
        commentID =  comment.id
        if commentID not in self.data["comment_ids"]:
            self.data["thread_ids"].append(threadid)
            self.data["comment_ids"].append(commentID)
            self.data["comment_body"].append(comment.body)
            self.data["ups"].append(comment.ups)
            self.data["downs"].append(comment.downs)
            self.data["author_ids"].append(comment.author_fullname[3:])
            self.data["created_utc"].append(comment.created_utc)
            self.data["edited"].append(comment.edited)

    def getLength(self):
        return len(self.data["comment_ids"])

    def saveData(self):
        super().saveData("CommentData.json")

    def loadData(self):
        self.data = super().loadData("CommentData.json")