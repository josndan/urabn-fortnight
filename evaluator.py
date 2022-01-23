from lib.ModelBuilder import *
from lib.Eval import *
from lib.Writer import *


builder = ModelBuilder()
evaluater = Eval()
bm25 = builder.getModel("bm25")
ql = builder.getModel("ql")
sdm = builder.getModel("sdm")
stress = builder.getModel("stress")

relvanceLis = bm25[1]

with open("./output/output.metrics", "w") as file:
    evaluater.setModel(bm25)
    EvalwriteOut(evaluater, list(bm25[0].keys()), file, "bm25.trecrun")

    evaluater.setModel(ql)
    EvalwriteOut(evaluater, list(ql[0].keys()), file, "ql.trecrun")

    evaluater.setModel(sdm)
    EvalwriteOut(evaluater, list(sdm[0].keys()), file, "sdm.trecrun")

    evaluater.setModel(stress)
    EvalwriteOut(evaluater, list(stress[0].keys()), file, "stress.trecrun")

#Report
with open("./output/report_bm25.csv","w") as f:
    for k in range(1,len(bm25[0]["450"])+1):
        evaluater.setModel(bm25)
        recall = evaluater.recall("450",k)
        percision = evaluater.P("450",k)
        f.write(f"{recall}, {percision}\n")


with open("./output/report_ql.csv","w") as f:
    for k in range(1, len(ql[0]["450"]) + 1):
        evaluater.setModel(ql)
        recall = evaluater.recall("450", k)
        percision = evaluater.P("450", k)
        f.write(f"{recall}, {percision}\n")

with open("./output/report_sdm.csv","w") as f:
    for k in range(1, len(sdm[0]["450"]) + 1):
        evaluater.setModel(sdm)
        recall = evaluater.recall("450", k)
        percision = evaluater.P("450", k)
        f.write(f"{recall}, {percision}\n")

with open("./output/report_stress.csv","w") as f:
    for k in range(1, len(stress[0]["450"]) + 1):
        evaluater.setModel(stress)
        recall = evaluater.recall("450", k)
        percision = evaluater.P("450", k)
        f.write(f"{recall}, {percision}\n")