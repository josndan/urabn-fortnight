import pandas as pd
import os.path as path
import pickle
import collections as c
import numpy as np
import math

class Web:
    def __init__(self, df):
        self.graph = {}
        count = 0
        for __, row in df.iterrows():
            if row[0] in self.graph:
                self.graph[row[0]].add(row[1])
            else:
                self.graph[row[0]] = set()
                if row[1] != "":
                    self.graph[row[0]].add(row[1])
            if row[1] != "" and row[1] not in self.graph:
                self.graph[row[1]] = set()

            count += 1
            if count % 100000 == 0:
                print(count)

    def countInlinks(self):
        print("Counting inlinks")
        self.inLinkCount = c.Counter()
        for outLinks in self.graph.values():
            for link in outLinks:
                self.inLinkCount[link] += 1

    def initIndex(self):
        print("Initializing indices")
        self.linkIndex = {}
        for index, link in enumerate(self.graph.keys()):
            self.linkIndex[link] = index
            self.linkIndex[index] = link
        x = 0
        return

    def diff(self, v1, v2):
        v=0
        for i in range(len(v1)):
            v+= (v1[i]-v2[i]) ** 2

        return math.sqrt(v)

    def computePageRank(self):
        self.initIndex()
        print("Computing PageRank")
        n = len(self.graph)
        tau = 0.0001
        lamb = 0.15

        initial = np.full(n, 1 / n)
        final = np.zeros(n)
        i = 1

        while True:
            print("Iteration " + str(i))
            final = np.full(n, lamb / n)
            numpage=1
            acc=0
            for page, links in self.graph.items():
                if numpage % 100000 == 0:
                    print("\t"*i + str(numpage))
                if len(links) > 0:
                    for p in links:
                        final[self.linkIndex[p]] += ((1 - lamb) / len(links)) * initial[self.linkIndex[page]]
                else:
                    acc += ((1 - lamb) / n) * initial[self.linkIndex[page]]
                numpage+=1

            final +=acc
            diff = self.diff(initial, final)
            print("Norm = "+str(diff),end="\n\n")
            if diff <= tau:
                break

            initial = final
            i += 1
        final = np.sort(final)[::-1]
        self.pageRank = final

    def writeInLinkCount(self):
        print("Writing out inlink counts")
        with open("inlinks.txt", "w+") as out:
            for rank, (link, count) in enumerate(self.inLinkCount.most_common(75)):
                out.write(link + " " + str(rank + 1) + " " + str(count) + "\n")

    def writePageRank(self):
        print("writing out pageranks")
        with open("pagerank.txt", "w+",encoding="utf-8") as out:
            for rank, score in enumerate(self.pageRank[:75]):
                out.write( str(self.linkIndex[rank]) + " " + str(rank + 1) + " " + str(score) + "\n")


webGraph = None

if path.exists("web.pkl"):
    with open("web.pkl", "rb") as f:
        webGraph = pickle.load(f)
else:
    df = pd.read_csv('links.srt.gz', compression='gzip', header=None, sep='\t')
    webGraph = Web(df)
    with open("web.pkl", "wb") as f:
        pickle.dump(webGraph, f, pickle.HIGHEST_PROTOCOL)

webGraph.countInlinks()
webGraph.writeInLinkCount()
webGraph.computePageRank()
webGraph.writePageRank()
