class Query:
    def __init__(self, data, res={}):
        self.res = res
        self.data = data

    def clear(self):
        self.res = {}

    def get(self):
        return self.res

    def documentAtTime(self, query, model):
        self.data.clearScore()
        # pLists = {}

        query = query.split()
        queryTermCount = {}
        # pointer = {}
        for term in query:
            if term in queryTermCount:
                queryTermCount[term] += 1
            else:
                queryTermCount[term] = 1


        # def skipTo(maxDocId, pointer, term):
        #     while pointer[term] < len(pLists[term]) and pLists[term][pointer[term]].getDocId() < maxDocId:
        #         pointer[term] += 1

        for doc in sorted(self.data.documents.values(), key=lambda x: x.docId):
            score = 0

            for term in query:
                if doc.docId in self.data.invertedIndex.db[term] :
                    score += model(term, doc, self.data, queryTermCount)
            doc.score = score

        return list(sorted(self.data.documents.values(), key=lambda x: x.score, reverse=True))

