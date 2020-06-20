from Data import Data
import praw


class AuthorData(Data):

    def __init__(self):
        super().__init__()
        self.data = {"author_ids": [], "comment_karma": [],
                     "link_karma": [], "created_utc": [], "is_premium": []}
        self.comment = None

    def retrieveData(self, comment):
        self.comment = comment
        if (self.checkAuthorAlreadyCollected()):
            pass
        else:
            try:
                self.retrieve()
            except praw.exceptions.RedditAPIException:
                return

    def checkAuthorAlreadyCollected(self):
        if (self.comment.author_fullname[3:] in self.getIds()):
            return True
        return False

    def retrieve(self):
        self.data["author_ids"].append(self.comment.author.id)
        self.data["comment_karma"].append(self.comment.author.comment_karma)
        self.data["link_karma"].append(self.comment.author.link_karma)
        self.data["created_utc"].append(self.comment.author.created_utc)
        self.data["is_premium"].append(self.comment.author.is_gold)

    def getIds(self):
        return self.data["author_ids"]

    def getLength(self):
        return len(self.data["author_ids"])

    def saveData(self):
        super().saveData("AuthorData.json")
    
    def loadData(self):
        self.data = super().loadData("AuthorData.json")