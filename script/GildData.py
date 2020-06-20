from Data import Data

class GildData(Data):

    def __init__(self):
        super().__init__()
        self.data= {"comment_ids": [], "gildings": []}  

    def retrieveData(self, comment):
        commentID =  comment.id
        if commentID not in self.data["comment_ids"]:
            self.data["comment_ids"].append(comment.id)
            self.data["gildings"].append(comment.gildings)

    def getLength(self):
        return len(self.data["comment_ids"])

    def saveData(self):
        super().saveData("GildData.json")
    
    def loadData(self):
        self.data = super().loadData("GildData.json")