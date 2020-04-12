#!/usr/bin/env python
# coding: utf-8

from os.path import isfile
import praw
import pandas as pd
from time import sleep
# Get credentials from DEFAULT instance in praw.ini
reddit = praw.Reddit()

class Scraper:

    # Checkpoint defines savepoints (save everytime n number of comments are collected).
    def __init__(self, sub_reddit, checkpoint=None, minimum=None):
        self.exectime = time.time()
        self.ids = []
        self.checkpoint = checkpoint
        self.interval = checkpoint
        self.minimum = minimum
        # By default, save everytime 5000 new comments are collected.
        if self.checkpoint is None:
            self.checkpoint = 10000
            self.interval = 10000
        if self.minimum is None:
            self.minimum = 200000
        if self.minimum < self.checkpoint:
            print("The minimum number (default: 200k) of records has to larger than checkpoint (default: 10k)")
            sys.exit()
        self.commentdata = {"comment_body": [],
                            "upvotes": []}
        self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(sub_reddit).top(limit=None)


        def retrieveComment(self, comment):
        """Takes in comment object as a parameter, which is used to obtain  comment body and number of upvotes.
        
        Note that some suspended users will still be retrieved (i.e. their comments will be added, however
        their accounts won't have suspended attribute, but will return a 404 error). We will have to remove
        such comments if the author information cannot be found from authors data table.
        """

        # Skip if the comment has been deleted or if the user is suspended/deleted.

        suspended = None
        try:
            suspended = comment.author.is_suspended
        except:
            pass
        if (comment.author is None or comment.body is None or suspended != None):
            pass
        else:
            self.commentdata["comment_body"].append(comment.body)
            self.commentdata["upvotes"].append(comment.score)
                    

    def addTo(self):
        """Takes the subreddit input from user as a parameter, calls respective method for retrieving relevant data."""

        for submission in self.subreddit:
            if (submission.id not in self.ids):
                self.ids.append(submission.id)
                submission.comments.replace_more(limit=None)
                all_comments = submission.comments.list()
                for comment in all_comments:
                    # comment.refresh()
                    self.retrieveComment(comment)
                self.save_files()

    def save_files(self):
        """Saves the files for every checkpoints, exits the program when minimum number of records is reached"""
        length  = len(self.commentdata["comment_ids"])
        if (length < self.checkpoint):
            pass
        else:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print("Collected {} records so far; Saving in progress. Time now: {}".format(length, current_time))
            data_f = pd.DataFrame(self.commentdata)
            authors_f = pd.DataFrame(self.author)
            gildings_f = pd.DataFrame(self.gildings)
            data_f.to_csv('../../data/raw/comment_data.csv', mode="w", index=False)
            authors_f.to_csv('../../data/raw/author_data.csv', mode="w", index=False)
            self.checkpoint += self.interval
        if (length > self.minimum):
            self.exectime = ((time.time() - self.exectime ) / (60*60))
            print("Collected {} records so far; Exiting now. Total execution time: {} hours".format(length, self.exectime))
            sys.exit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sub_reddit", help="Specify the subreddit to scrape from")
    parser.add_argument("-m", "--minimum", help="Specify the minimum number of data records to collect",
                        type=int)
    parser.add_argument("-c", "--checkpoint",
                        help="Save the file every c comments", type=int)
    args = parser.parse_args()
    if (args.minimum and args.checkpoint):
        Scraper(args.sub_reddit, checkpoint=args.checkpoint,
                 minimum=args.minimum).addTo()
    if (args.minimum):
        Scraper(args.sub_reddit, minimum=args.minimum).addTo()
    if (args.checkpoint):
        Scraper(args.sub_reddit, checkpoint=args.checkpoint).addTo()
    Scraper(args.sub_reddit).addTo()


if __name__ == "__main__":
    main()