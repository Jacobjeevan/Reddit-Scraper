import pandas as pd
import argparse
from CommentData import CommentData
from AuthorData import AuthorData
from GildData import GildData
from ThreadData import ThreadData
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import StratifiedShuffleSplit
from pathlib import Path


class preprocess:

    def __init__(self, args):
        self.initializeDataObjects()
        self.loadpath = "../../data/raw/"
        self.savepath = args.savepath
        if args.loadpath != "../../data/raw/":
            self.loadpath = args.loadpath
            self.setDifferentLoadpath()
        self.loadData()
        self.convertToPandas()
        self.MergedData = None

    def initializeDataObjects(self):
        self.threaddata = ThreadData()
        self.commentdata = CommentData()
        self.gilddata = GildData()
        self.authordata = AuthorData()
        
    def setDifferentLoadpath(self):
        self.threaddata.setpath(self.loadpath)
        self.commentdata.setpath(self.loadpath)
        self.gilddata.setpath(self.loadpath)
        self.authordata.setpath(self.loadpath)

    def loadData(self):
        self.threaddata.loadData()
        self.commentdata.loadData()
        self.gilddata.loadData()
        self.authordata.loadData()
    
    def convertToPandas(self):
        self.threaddata = pd.DataFrame(self.threaddata.getData())
        self.commentdata = pd.DataFrame(self.commentdata.getData())
        self.gilddata = pd.DataFrame(self.gilddata.getData())
        self.authordata = pd.DataFrame(self.authordata.getData())

    def process(self):
        self.handleErrorCases()
        self.threaddata.drop(["author_ids"], axis=1, inplace=True)
        self.mergeData()

    def handleErrorCases(self):
        self.authordata = self.dropDuplicatesAndEmptyRows(self.authordata, ['author_ids'])
        self.commentdata = self.dropDuplicatesAndEmptyRows(self.commentdata, ['comment_ids'])
        self.gilddata = self.dropDuplicatesAndEmptyRows(self.gilddata, ['comment_ids'])
        self.threaddata = self.dropDuplicatesAndEmptyRows(self.threaddata, ['thread_ids'])

    def dropDuplicatesAndEmptyRows(self, data, key_columns):
        df = data.copy()
        df.drop_duplicates(subset=key_columns, keep='last', inplace=True, ignore_index=True)
        return df.dropna()

    def mergeData(self):
        commentsAndThreads = self.mergeCommentsAndThreads()
        self.mergeWithGilds(commentsAndThreads)
        transformGilds = gildsToBinary()
        self.MergedData, self.targets = transformGilds.transform(self.MergedData)
    
    def mergeCommentsAndThreads(self):
        commentsAndThreads = self.commentdata.merge(self.threaddata, how="left", on="thread_ids", suffixes=("_comment", "_thread"))
        commentsAndThreads.dropna(inplace=True)
        commentsAndThreads["comment_age"] =  commentsAndThreads["created_utc_comment"] - commentsAndThreads["created_utc_thread"]
        commentsAndThreads = commentsAndThreads.filter(["comment_body", "ups", "comment_ids", "edited_comment", "upvotes"
        , "premium", "num_comments", "author_ids", "comment_age"], axis=1)
        commentsAndThreads = commentsAndThreads.rename(columns={"upvotes":"Thread_upvotes", "ups":"comment_upvotes"})
        return commentsAndThreads

    def mergeWithGilds(self, commentsAndThreads):
        commentsThreadsGilds = self.gilddata.merge(commentsAndThreads, how='outer', on='comment_ids')
        self.MergedData = commentsThreadsGilds.merge(self.authordata, how='inner', on='author_ids')

    def splitAndSave(self):
        splits = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        for train_index, test_index in splits.split(self.MergedData, self.targets):
            pass
        trainSet = self.MergedData.iloc[train_index, :]
        testSet = self.MergedData.iloc[test_index, :]
        trainSet.reset_index(drop=True, inplace=True)
        testSet.reset_index(drop=True, inplace=True)
        self.saveJson(trainSet, "trainSet_baseline")
        self.saveJson(testSet, "testSet_baseline")

    def saveJson(self, df, filename):
        Path(self.savepath).mkdir(parents=True, exist_ok=True)
        filename = f"{self.savepath}{filename}.json"
        df.to_json(filename, orient="columns")
        
class gildsToBinary(BaseEstimator, TransformerMixin):
    '''Using Sklearn's base transformer class to process the gildings column (convert the dictionary into binary)'''
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        df = X.copy()
        df["gildings"].fillna(0, inplace=True)
        df["gildings"] = df["gildings"].apply(lambda x: 1 if x != 0 else 0)
        return df, df["gildings"]

def build_parser():
    loadpath = "../../data/raw/"
    savepath = "../../data/processed/"
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loadpath",
                        help="Load folder for raw files", type=str, default=loadpath)
    parser.add_argument("-s", "--savepath",
                        help="Save folder for processed files", type=str, default=savepath)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    Preprocess = preprocess(args)
    Preprocess.process()
    Preprocess.splitAndSave()

if __name__ == "__main__":
    main()