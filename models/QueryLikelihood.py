import math


def QL(term, doc, data, queryTermCount, mu=300):
    f = 0
    for posting in data.invertedIndex.db[term].values():
        if posting.docId == doc.docId:
            f += posting.getTermCount()
            break
    c = data.termCount[term]
    C = data.totalTermCount
    D = doc.length

    res = math.log((f + mu * c / C) / (D + mu))

    return res
