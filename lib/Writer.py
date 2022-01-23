def writeOut(data, query,queries, model, fileName,top):
    runTag = f"jselvaraaj-{fileName}"
    with open(f"./output/{fileName}.trecrun", "w") as f:
        for i, q in enumerate(queries):
            rank = 1
            for doc in query.documentAtTime(q, model):
                space = " " * (int(data.maxSceneLen) + 10 - len(doc.sceneId))

                if doc.score != 0 :
                    if rank <= 10 and i == 4:
                        top.add(doc.sceneId)
                    f.write(f"Q{i + 1} skip {doc.sceneId}" + space + f"{rank} {doc.score} {runTag}\n")
                    rank+=1

def EvalwriteOut(evaluater, queries, file, name):
    print(name)
    ndcg, p_5, p_20, recall, f_1 = 0, 0, 0, 0, 0
    l = len(queries)
    map = evaluater.MAP()
    mrr = evaluater.MRR()
    for query in queries:
        ndcg += evaluater.NDCG(query, 10)
        p_5 += evaluater.P(query, 5)
        p_20 += evaluater.P(query, 20)
        recall += evaluater.recall(query, 20)
        f_1 += evaluater.F1(query, 20)

    ndcg, p_5, p_20, recall, f_1 = ndcg / l, p_5 / l, p_20 / l, recall / l, f_1 / l
    file.write(f"{name} NDCG@10 {ndcg}\n")
    file.write(f"{name} P@5 {p_5}\n")
    file.write(f"{name} P@20 {p_20}\n")
    file.write(f"{name} Recall@20 {recall}\n")
    file.write(f"{name} F_1@20 {f_1}\n")
    file.write(f"{name} MAP {map}\n")
    file.write(f"{name} MRR {mrr}\n")