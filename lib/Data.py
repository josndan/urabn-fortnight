import json
from lib.InvertedIndex import *
from lib.Document import *
from lib.Posting import *

class Data:
    def __init__(self):
        self.documents = {}
        self.invertedIndex = InvertedIndexDB()
        self.avgDocLen = 0
        self.totalTermCount = 0
        self.termCount = {}
        self.maxSceneLen = float("-inf")
        self.dataLoader()

    def clearScore(self):
        for doc in self.documents.values():
            doc.score = 0

    def getScenesByDoc(self, docIds):
        res = set()
        for id in docIds:
            res.add(self.documents[id].getSceneId())
        return sorted(list(res))

    def getPlaysByDoc(self, docIds):
        res = set()
        for id in docIds:
            res.add(self.documents[id].getPlayId())
        return sorted(list(res))

    def dataLoader(self):
        invertedIndex = self.invertedIndex
        jData = json.load(open("./res/shakespeare-scenes.json"))
        docId = 0
        sumDocLen = 0
        for scence in jData["corpus"]:
            docId += 1
            invertedIndex.key[scence["sceneId"]] = docId
            self.maxSceneLen = max(self.maxSceneLen, len(scence["sceneId"]))
            tokens = scence["text"].split()
            docLen = len(tokens)
            sumDocLen += docLen

            position = 0
            table = {}
            for token in tokens:
                if token == "":
                    continue
                position += 1
                if token in table:
                    table[token].append(position)
                else:
                    table[token] = [position]
                if token in self.termCount:
                    self.termCount[token] += 1
                else:
                    self.termCount[token] = 1

            self.documents[docId] = Document(docId, scence["playId"], scence["sceneId"], scence["sceneNum"],
                                             scence["text"], docLen)

            for term in table:
                posting = Posting(docId, (scence["sceneId"], scence["playId"]), table[term])
                invertedIndex.addPosting(term, posting,docId)
        avg = sumDocLen / len(self.documents)
        self.totalTermCount = sumDocLen
        self.avgDocLen = avg