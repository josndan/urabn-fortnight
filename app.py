from lib.Data import *
from lib.Query import *
from lib.Writer import *
from models.BM25 import *
from models.QueryLikelihood import *

data = Data()
query = Query(data)
queries = ["the king queen royalty"
    , "servant guard soldier"
    , "hope dream sleep"
    , "ghost spirit"
    , "fool jester player"
    , "to be or not to be"]

top = set()

writeOut(data, query, queries, BM25, "bm25" ,top)

writeOut(data, query, queries, QL, "ql" ,top)
