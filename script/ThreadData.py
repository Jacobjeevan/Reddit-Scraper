from Data import Data
import praw


class ThreadData(Data):

    def __init__(self):
        super().__init__()
        self.length = 0
        self.thread = None
        self.clearData()

    def clearData(self):
        self.data = {"thread_ids": [], "title": [], "author_ids": [], "upvotes": [
        ], "gildings": [], "created_utc": [], "premium": [], "num_comments": [], "edited": []}

    def retrieveData(self, thread):
        self.thread = thread
        threadID = self.thread.id
        if (super().IfAlreadyCollected(threadID)):
            pass
        else:
            self.retrieve(threadID)

    def retrieve(self, threadID):
        self.length += 1
        self.retrieveThreadAuthor()
        self.data["thread_ids"].append(threadID)
        super().addToTracker(threadID)
        self.data["title"].append(self.thread.title)
        self.data["upvotes"].append(self.thread.ups)
        self.data["edited"].append(self.thread.edited)
        self.data["gildings"].append(self.thread.gildings)
        self.data["created_utc"].append(self.thread.created_utc)
        self.data["num_comments"].append(self.thread.num_comments)

    def retrieveThreadAuthor(self):
        try:
            self.data["author_ids"].append(self.thread.author_fullname[3:])
            self.data["premium"].append(self.thread.author_premium)
        except praw.exceptions.RedditAPIException:
            self.data["author_ids"].append("NaN")
            self.data["premium"].append("NaN")

    def saveData(self):
        super().saveData("ThreadData.json")
        self.clearData()

    def loadData(self):
        self.data = super().loadData("ThreadData.json")
