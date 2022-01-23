class ModelBuilder:
    def getModel(self, name):
        model = {}
        rel = {}
        with open("./evaluation-data/qrels", "r") as f:
            for line in f:
                queryNo, _, docId, jud = tuple(line.split())
                if queryNo not in rel:
                    rel[queryNo] = {docId: int(jud)}
                else:
                    rel[queryNo][docId] = int(jud)
        with open("./evaluation-data/" + name + ".trecrun", "r") as f:
            for line in f:
                queryNo, _, docId, rank, score, __ = tuple(line.split())
                if queryNo not in model:
                    model[queryNo] = [(docId, int(rank))]
                else:
                    model[queryNo].append((docId, int(rank)))

        for queryNo in model.keys():
            model[queryNo] = list(sorted(model[queryNo], key=lambda x: x[1]))
        return (model, rel)