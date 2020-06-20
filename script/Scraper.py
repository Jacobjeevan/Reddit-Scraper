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

    def __init__(self, args):
        """Parse the arguments"""
        self.exectime = time.time()
        self.interval = args.checkpoint
        self.checkpoint = args.checkpoint
        self.minimum = args.minimum 
        if self.minimum < self.checkpoint:  # Ensure that minimum is greater than checkpoint
            print(
                f"The minimum number of records ({self.minimum}), has to larger than checkpoint ({self.checkpoint})")
            sys.exit()
        self.initializeDataObjects()
        # Initializing the praw reddit object and calling it.
        self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(args.subreddit).top(limit=None)
        # Default save path of the data.
        self.savepath = "../../data/raw/"
        if args.savepath != "../../data/raw/":
            self.savepath = args.savepath
            self.setDifferentSavepath()
        if args.load:
            self.loadExistingData()
            self.checkpoint = self.commentdata.getLength()    

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
                print(f"Already collected {submission.num_comments} comments")
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
        if (numOfSamples < self.checkpoint):
            pass
        else:
            self.checkSaveConditions(numOfSamples)
        self.checkExitConditions(numOfSamples)

    def checkSaveConditions(self, numOfSamples):
        exectime = self.getElaspedTime()
        print("Collected {} comments so far; Saving in progress. Time elapsed: {} hours".format(
            numOfSamples, exectime))
        self.saveAllData()
        self.checkpoint += self.interval

    def saveAllData(self):
        self.authordata.saveData()
        self.commentdata.saveData()
        self.gilddata.saveData()
        self.threaddata.saveData()

    def checkExitConditions(self, numOfSamples):
        if (numOfSamples >= self.minimum):
            exectime = self.getElaspedTime()
            print("Collected {} comments so far; Total execution time: {} hours".format(
                numOfSamples, exectime))
            self.exitPrompts()

    def getElaspedTime(self):
        return ((time.time() - self.exectime) / (60*60))

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
    CHECKPOINT = 10000
    SAVEPATH = "../../data/raw/"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "subreddit", help="Specify the subreddit to scrape from")
    parser.add_argument("-m", "--minimum", 
    help="Specify the minimum number of data records to collect. If load file option is used, then minimum will include comment length from loaded file.",
                        type=int, default=MINIMUM)
    parser.add_argument("-c", "--checkpoint",
                        help="Save the file every c comments", type=int, default=CHECKPOINT)
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
