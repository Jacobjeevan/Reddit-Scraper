#! usr/bin/env python3
import sys
import praw
import time
import argparse
import json
from CommentData import CommentData
from AuthorData import AuthorData
from GildData import GildData
from ThreadData import ThreadData


class Scraper:

    def __init__(self, args):
        self.exectime = time.time()
        self.initializeDataObjects()
        # Default save path of the data.
        self.savepath = "data/raw/"
        self.parseArgs(args)

    def parseArgs(self, args):
        self.minimum = args.minimum
        if self.savepath != args.savepath:
            self.savepath = args.savepath
            self.setDifferentSavepath()
        if args.load:
            self.loadExistingData()
        self.gui = args.gui
        if (self.gui):
            with open("src/prawConfig.json", "r") as jsonfile:
                data = json.load(jsonfile)
            self.reddit = praw.Reddit(client_id=data["clientID"],
                                      client_secret=data["clientSecret"],
                                      user_agent=data["useragent"],
                                      username=data["username"],
                                      password=data["password"])
        else:
            self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(args.subreddit).top(limit=None)

    def initializeDataObjects(self):
        self.threaddata = ThreadData()
        self.commentdata = CommentData()
        self.gilddata = GildData()
        self.authordata = AuthorData()

    def setDifferentSavepath(self):
        self.threaddata.setpath(self.savepath)
        self.commentdata.setpath(self.savepath)
        self.gilddata.setpath(self.savepath)
        self.authordata.setpath(self.savepath)

    def loadExistingData(self):
        self.threaddata.loadData()
        self.commentdata.loadData()
        self.gilddata.loadData()
        self.authordata.loadData()

    def scrape(self):
        subreddit = self.subreddit
        self.numOfSamples = self.commentdata.getLength()
        interval = 50
        checkpoint = self.numOfSamples+interval
        for submission in subreddit:
            self.threaddata.retrieveData(submission)
            submission.comments.replace_more(limit=None)
            all_comments = submission.comments.list()
            for comment in all_comments:
                self.retrieveAll(comment, submission.id)
                if (self.numOfSamples == checkpoint and self.gui):
                    # Print numOfSamples collected with interval of 50 samples
                    self.printMessage()
                    checkpoint += interval
                    self.checkSaveConditions()
                    self.checkExitConditions()

    def retrieveAll(self, comment, threadid):
        if (self.checkAuthorOrCommentIsDeleted(comment) or self.checkIfAuthorIsSuspended(comment)):
            pass
        else:
            self.authordata.retrieveData(comment)
            self.numOfSamples += self.commentdata.retrieveData(
                comment, threadid)
            if comment.gildings:
                self.gilddata.retrieveData(comment)

    def checkAuthorOrCommentIsDeleted(self, comment):
        if (comment.author is None or comment.body is None):
            return True
        return False

    def checkIfAuthorIsSuspended(self, comment):
        try:
            _ = comment.author.is_suspended
            return True
        except AttributeError:
            pass
        return False

    def checkSaveConditions(self):
        self.printMessage()
        self.saveAllData()

    def saveAllData(self):
        self.authordata.saveData()
        self.commentdata.saveData()
        self.gilddata.saveData()
        self.threaddata.saveData()

    def checkExitConditions(self):
        if (self.numOfSamples >= self.minimum):
            if self.gui:
                self.exitPromptsForGUI()
            else:
                self.exitPrompts()

    def printMessage(self):
        if self.gui:
            print(self.numOfSamples)
        else:
            exectime = self.getElapsedTime()
            print(
                f"{self.numOfSamples} collected so far. Elapsed Time: {exectime} hours")

    def getElapsedTime(self):
        return round(((time.time() - self.exectime) / (60*60)), 3)

    def exitPrompts(self):
        flag = True
        while (flag):
            val = input(
                "Would you like to exit now? Press Y/N; N allows to continue scraping.\n")
            if (val.lower() == 'y'):
                sys.exit()
            elif (val.lower() == 'n'):
                print(f"Current minimum is {self.minimum}\n")
                try:
                    MoreComments = int(
                        input("How many more comments do you want to collect?\n"))
                    self.minimum += MoreComments
                    flag = False
                except TypeError:
                    print("Wrong type of input. Please enter valid input.\n")
                    continue
            else:
                print("Wrong type of input. Please enter valid input.\n")

    def exitPromptsForGUI(self):
        print("Done")
        sys.exit()


def build_parser():
    """Parser to grab and store command line arguments"""
    MINIMUM = 200000
    SAVEPATH = "../data/raw/"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "subreddit", help="Specify the subreddit to scrape from")
    parser.add_argument("-m", "--minimum",
                        help="Specify the minimum number of data records to collect. If load file option is used, then minimum will include comment length from loaded file.",
                        type=int, default=MINIMUM)
    parser.add_argument("-s", "--savepath",
                        help="Save/load folder", type=str, default=SAVEPATH)
    parser.add_argument("-l", "--load",
                        help="Load existing samples to continue scraping", action="store_true")
    parser.add_argument("-g", "--gui",
                        help="Call this flag when running from Javascript GUI", action="store_true")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    Scraper(args).scrape()


if __name__ == "__main__":
    main()
