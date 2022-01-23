import math


class Eval:
    def setModel(self, mod):
        self.model, self.rel = mod

    def MRR(self):
        sum = 0
        for query in self.model:
            sum += self.RR(query)
        return sum / len(self.model)

    def MAP(self):
        sum = 0
        for query in self.model:
            sum += self.AP(query)
        return sum / len(self.model)

    def NDCG(self, query, k):
        num = self.DCG(k, self.model[query], self.rel[query])
        deno = self.DCG(k, list(sorted(self.rel[query].items(), key=lambda x: x[1], reverse=True)), self.rel[query])
        return num / deno

    def DCG(self, k, L, R):
        res = 0
        if L[0][0] in R:
            res = R[L[0][0]]
        i = 2
        for item in L[1:k]:
            if item[0] in R:
                res += R[item[0]] / math.log(i, 2)
            i += 1
        return res

    def RR(self, query):
        res = 0
        for item in self.model[query]:
            if item[0] in self.rel[query] and self.rel[query][item[0]] > 0:
                res = 1 / item[1]
                break
        return res

    def P(self, query, k):
        inter = []
        for item in self.model[query][:k]:
            if item[0] in self.rel[query] and self.rel[query][item[0]] > 0:
                inter.append(item)
        return len(inter) / k

    def recall(self, query, k):
        inter = []
        for item in self.model[query][:k]:
            if item[0] in self.rel[query] and self.rel[query][item[0]] > 0:
                inter.append(item)
        div = 0
        for key in self.rel[query]:
            if self.rel[query][key] > 0:
                div += 1

        return len(inter) / div

    def F1(self, query, k):
        R = self.recall(query, k)
        P = self.P(query, k)
        if R + P == 0:
            return 0
        return 2 * R * P / (R + P)

    def AP(self, query):
        ap = 0
        i = 0
        for item in self.model[query]:
            if item[0] in self.rel[query] and self.rel[query][item[0]] > 0:
                ap += self.P(query, i + 1)
            i += 1

        div = 0
        for key in self.rel[query]:
            if self.rel[query][key] > 0:
                div += 1

        return ap / div