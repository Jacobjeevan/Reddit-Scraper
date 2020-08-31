import json
import os
from pathlib import Path


class Data:

    def __init__(self):
        super().__init__()
        self.data = {}
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
        if (os.path.exists(filename)):
            self.data = self.appendToExistingFile(filename)
        json.dump(self.data, open(filename, "w"))

    def appendToExistingFile(self, filename):
        with open(filename, "r") as readFile:
            data = json.load(readFile)
            for key in data:
                if self.data[key] != []:
                    data[key].extend(self.data[key])
        return data

    def clearData(self):
        pass

    def loadData(self, filename):
        filename = self.savepath + filename
        with open(filename, "r") as write_file:
            data = json.load(write_file)
        self.length = len(data)
        return data

    def getData(self):
        return self.data

    def addToTracker(self, record):
        self.tracker.append(record)

    def IfAlreadyCollected(self, record):
        if record in self.tracker:
            return True
        return False
