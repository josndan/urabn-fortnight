import math


def BM25(term, doc, data, queryTermCount, k_1=1.2, k_2=10, b=0.85):
    N = len(data.documents)
    n = len(data.invertedIndex.db[term])
    f = 0
    for posting in data.invertedIndex.db[term].values():
        if posting.docId == doc.docId:
            f += posting.getTermCount()
            break

    qf = queryTermCount[term]
    K = k_1 * ((1 - b) + b * doc.length / data.avgDocLen)
    res = math.log((N - n + 0.5) / (n + 0.5), 10) * ((k_1 + 1) * f / (K + f)) * ((k_2 + 1) * qf / (k_2 + qf))

    return res
