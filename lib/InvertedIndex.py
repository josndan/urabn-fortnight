class InvertedIndexDB:
    def __init__(self):
        self.db = {}
        self.docCount = 0
        self.key = {}
        # self.pointer={}

    def addPosting(self, term, posting, docId):
        if term in self.db:
            self.db[term][docId] = posting
            # self.pointer[term] = 0
        else:
            self.db[term] = {docId: posting}
        self.docCount += 1

    def getVocabSize(self):
        return len(self.db)

    def getDB(self):
        return self.db

    def getTermCollectionFreq(self, term):
        sum = 0
        for posting in self.db[term]:
            sum += posting.getTermCount()
        return sum

    def getTermDocumentFreq(self, term):
        return len(self.db[term])

    def getDocCount(self):
        return self.docCount

    def getVocab(self):
        return self.db.keys()
