from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from functools import lru_cache
import math
import os
from colbert import Searcher
from colbert.data import Collection
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Date, Text, JSON, ForeignKey, Enum, TIMESTAMP
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
counter = {"api" : 0}

#set up sqlite
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
db.init_app(app)

#set up Searcher instance
INDEX_DIR = "backend/db/experiments/ver1/indexes"
nbits = 2   # encode each dimension with 2 bits
doc_maxlen = 300   # truncate passages at 300 tokens
index_name = f'{nbits}bits'
collection = Collection("backend/db/contexts.tsv")
searcher = Searcher(index=index_name, index_root=INDEX_DIR, collection=collection)

#service layer
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

def api_request_data(lang):
    pass

#api layer
@app.route("/api/search", methods=["GET"])
def api_search():
    if request.method == "GET":
        counter["api"] += 1
        print("API request count:", counter["api"])
        return api_search_query(request.args.get("query"), request.args.get("k"))
    else:
        return ('', 405)

@app.route("/api/data", methods=["GET"])
def api_data():
    if request.method == "GET":
        return api_request_data(request.args.get("lang"))
    
class Context(db.Model, SerializerMixin):
    __tablename__ = "context"
    id = mapped_column(Integer, primary_key=True, nullable=False)
    context = mapped_column(String, nullable=False)
    lang = mapped_column(String, nullable=False)

class Query(db.Model, SerializerMixin):
    __tablename__ = "query"
    id = mapped_column(Integer, primary_key=True, nullable=False)
    context_id = mapped_column(Integer, ForeignKey("context.id"), nullable=False)
    query = mapped_column(String, nullable=False)

if __name__ == "__main__":
    app.run("0.0.0.0", int(os.getenv("PORT")))
