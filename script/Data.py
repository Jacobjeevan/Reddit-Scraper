import json
import os
from pathlib import Path


class Data:

    def __init__(self):
        super().__init__()
        self.data = None
        self.dirname = os.path.dirname(__file__)
        self.length = 0
        self.savepath = "../../data/raw/"
        self.tracker = []

    def getLength(self):
        return self.length

    def setpath(self, savepath):
        self.savepath = savepath

    def saveData(self, filename):
        filename = self.savepath + filename
        json.dump(self.data, open(filename, "a"))

    def clearData(self):
        pass

    def loadData(self, filename):
        filename = self.savepath + filename
        with open(filename, "r") as write_file:
            data = json.load(write_file)
        return data

    def getData(self):
        return self.data

    def addToTracker(self, id):
        self.tracker.append(id)

    def getTracker(self):
        return self.tracker
