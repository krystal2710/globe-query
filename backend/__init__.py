from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from functools import lru_cache
import math
import os
from dotenv import load_dotenv

from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Searcher
from colbert.data import Collection

load_dotenv()

app = Flask(__name__)
counter = {"api" : 0}

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/data.sqlite"
db.init_app(app)


INDEX_DIR = "backend/db/experiments/testing/indexes"
nbits = 2   # encode each dimension with 2 bits
doc_maxlen = 300   # truncate passages at 300 tokens
index_name = f'{nbits}bits'
import sys
print(sys.path)
collection = Collection("backend/db/contexts.tsv")
# with Run().context(RunConfig(experiment=INDEX_DIR)):
searcher = Searcher(index=index_name, index_root=INDEX_DIR, collection=collection)
# checkpoint = '/Volumes/Users/ly_k1/Documents/mColBERT/experiments/default/none/2024-04/13/23.13.02/checkpoints/colbert'

@lru_cache(maxsize=1000000)
def api_search_query(query, k):
    print(f"Query={query}")
    if k == None: k = 10
    k = min(int(k), 100)
    pids, ranks, scores = searcher.search(query, k=100)
    pids, ranks, scores = pids[:k], ranks[:k], scores[:k]
    passages = [searcher.collection[pid] for pid in pids]
    probs = [math.exp(score) for score in scores]
    probs = [prob / sum(probs) for prob in probs]
    topk = []
    for pid, rank, score, prob in zip(pids, ranks, scores, probs):
        text = searcher.collection[pid]            
        d = {'text': text, 'pid': pid, 'rank': rank, 'score': score, 'prob': prob}
        topk.append(d)
    topk = list(sorted(topk, key=lambda p: (-1 * p['score'], p['pid'])))
    return {"query" : query, "topk": topk}

@app.route("/api/search", methods=["GET"])
def api_search():
    if request.method == "GET":
        counter["api"] += 1
        print("API request count:", counter["api"])
        return api_search_query(request.args.get("query"), request.args.get("k"))
    else:
        return ('', 405)

if __name__ == "__main__":
    app.run("0.0.0.0", int(os.getenv("PORT")))
