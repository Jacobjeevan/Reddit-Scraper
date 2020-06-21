#! usr/bin/env python3
import sys
import praw
import time
import argparse
from CommentData import CommentData
from AuthorData import AuthorData
from GildData import GildData
from ThreadData import ThreadData

class Scraper:

    def __init__(self, args=None, subreddit=None, minimum=None, savepath=None, loadpath=None):
        self.exectime = time.time()
        self.initializeDataObjects()
        self.reddit = praw.Reddit()
        # Default save path of the data.
        self.savepath = "../data/raw/"
        if args:
            self.parseArgs(args)
        else:
            self.subreddit = self.reddit.subreddit(subreddit).top(limit=None)
            self.minimum = minimum
            if (savepath and savepath != "../data/raw/"):
                self.savepath = savepath
                self.setDifferentSavepath()
            if loadpath:
                self.loadpath = loadpath
                self.loadExistingData()
        
    def parseArgs(self, args):
        self.minimum = args.minimum
        self.subreddit = self.reddit.subreddit(args.subreddit).top(limit=None)
        if args.savepath != "../data/raw/":
            self.savepath = args.savepath
            self.setDifferentSavepath()
        if args.load:
            self.loadExistingData()


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
        for submission in subreddit:
            if (submission.id in self.threaddata.getIds()):
                pass
            else:
                self.threaddata.retrieveData(submission)
                submission.comments.replace_more(limit=None)
                all_comments = submission.comments.list()
                for comment in all_comments:
                    self.retrieveAll(comment, submission.id)
                self.saveOrExitConditions()

    def retrieveAll(self, comment, threadid):
        if (self.checkAuthorOrCommentIsDeleted(comment) or self.checkIfAuthorIsSuspended(comment)):
            pass
        else:
            self.authordata.retrieveData(comment)
            self.commentdata.retrieveData(comment, threadid)
            if comment.gildings:
                self.gilddata.retrieveData(comment)

    def checkAuthorOrCommentIsDeleted(self, comment):
        if (comment.author is None or comment.body is None):
            return True
        return False

    def checkIfAuthorIsSuspended(self, comment):
        IsSuspended = None
        try:
            IsSuspended = comment.author.is_suspended
        except praw.exceptions.RedditAPIException:
            pass
        if (IsSuspended):
            return True
        return False

    def saveOrExitConditions(self):
        numOfSamples = self.commentdata.getLength()
        self.checkSaveConditions(numOfSamples)
        self.checkExitConditions(numOfSamples)

    def checkSaveConditions(self, numOfSamples):
        exectime = self.getElaspedTime()
        print(numOfSamples, " ", exectime)
        self.saveAllData()

    def saveAllData(self):
        self.authordata.saveData()
        self.commentdata.saveData()
        self.gilddata.saveData()
        self.threaddata.saveData()

    def checkExitConditions(self, numOfSamples):
        if (numOfSamples >= self.minimum):
            exectime = self.getElaspedTime()
            print(numOfSamples, " ", exectime)
            self.exitPrompts()

    def getElaspedTime(self):
        return round(((time.time() - self.exectime) / (60*60)),3)

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


def build_parser():
    """Parser to grab and store command line arguments"""
    MINIMUM = 200000
    SAVEPATH = "../data/raw/"
    parser = argparse.ArgumentParser()
    parser.add_argument("subreddit", help="Specify the subreddit to scrape from")
    parser.add_argument("-m", "--minimum", 
    help="Specify the minimum number of data records to collect. If load file option is used, then minimum will include comment length from loaded file.",
                        type=int, default=MINIMUM)
    parser.add_argument("-s", "--savepath",
                        help="Save/load folder", type=str, default=SAVEPATH)
    parser.add_argument("-l", "--load",
                        help="Load existing samples to continue scraping", type=bool, default=False)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    Scraper(args).scrape()

if __name__ == "__main__":
    main()