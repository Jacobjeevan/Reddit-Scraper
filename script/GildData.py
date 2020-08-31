from .Data import Data


class GildData(Data):

    def __init__(self):
        super().__init__()
        self.length = 0
        self.comment = None
        self.clearData()

    def clearData(self):
        self.data = {"comment_ids": [], "gildings": []}

    def retrieveData(self, comment):
        self.comment = comment
        commentID = self.comment.id

        if (super().IfAlreadyCollected(commentID)):
            pass
        else:
            self.retrieve(commentID)

    def retrieve(self, commentID):
        self.length += 1
        super().addToTracker(commentID)
        self.data["comment_ids"].append(commentID)
        self.data["gildings"].append(self.comment.gildings)

    def saveData(self):
        super().saveData("GildData.json")
        self.clearData()

    def loadData(self):
        self.data = super().loadData("GildData.json")
