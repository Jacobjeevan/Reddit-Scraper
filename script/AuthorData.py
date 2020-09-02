from .Data import Data
import praw


class AuthorData(Data):

    def __init__(self):
        super().__init__()
        self.clearData()
        self.length = 0
        self.comment = None

    def clearData(self):
        self.data = {"author_ids": [], "comment_karma": [],
                     "link_karma": [], "created_utc": [], "is_premium": []}

    def retrieveData(self, comment):
        self.comment = comment
        authorID = self.comment.author_fullname[3:]
        if (super().IfAlreadyCollected(authorID)):
            pass
        else:
            try:
                self.retrieve(authorID)
            except praw.exceptions.RedditAPIException:
                return

    def retrieve(self, authorID):
        self.length += 1
        super().addToTracker(authorID)
        self.data["author_ids"].append(authorID)
        self.data["comment_karma"].append(self.comment.author.comment_karma)
        self.data["link_karma"].append(self.comment.author.link_karma)
        self.data["created_utc"].append(self.comment.author.created_utc)
        self.data["is_premium"].append(self.comment.author.is_gold)

    def saveData(self):
        super().saveData("AuthorData.json")
        self.clearData()

    def loadData(self):
        super().loadData("AuthorData.json")
        super().setMetaData("author_ids")
