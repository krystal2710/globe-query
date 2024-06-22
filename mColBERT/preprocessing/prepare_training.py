import jsonlines
import json
import os
import sys
from dotenv import load_dotenv
import random
load_dotenv()
sys.path.append(os.getenv('ROOT_DIR'))

def create_triples(data_filepath, data_neg_filepath, removed_queries):
    print("Creating triples from {data_filepath} and {data_neg_filepath}".format(data_filepath = data_filepath, data_neg_filepath = data_neg_filepath))

    #Read the query-context jsonl file
    with open(data_filepath, "r") as data_file:
        reader = jsonlines.Reader(data_file)
        data = []
        for line in reader:
            if line["query_id"] not in removed_queries:
                data.append(line)
        
    #Read the query-negative context file
    contexts = set()
    with open(data_neg_filepath, "r") as data_neg_file:
        data_neg = {}
        json_raw = json.load(data_neg_file)["data"]
        for line in json_raw:
            if line["query_id"] not in data_neg:
                data_neg[line["query_id"]] = []
            data_neg[line["query_id"]].append(line["context_id"])
            contexts.add(line["context_id"])
    contexts = list(contexts)
    #Open triples file
    triples = []

    #iterate through each query
    n = len(data)
    count_not_found = 0
    count_triples = 0
    for i, row in enumerate(data):
        qid = row["query_id"]
        pos_pid = row["context_id"]
        try:
            neg_pid_list = data_neg[row["orig_query_id"]]
        except:
            count_not_found += 1
            random_neg_pid= random.choice(contexts)
            while random_neg_pid==pos_pid:
                random_neg_pid= random.choice(contexts)
            neg_pid_list = [random_neg_pid]
        finally:
            #iterate through each negative context
            for neg_pid in neg_pid_list:
                triple = [qid, pos_pid, neg_pid]
                triples.append(triple)
                count_triples += 1

    print("Created {i} triples".format(i = count_triples))
    print("There are {i}/{total} not found queries".format(i=count_not_found, total=n))
    return triples

def create_all_triples(input_dir, output_dir, removed_queries):
    triples_file = open(os.path.join(output_dir,"triples.jsonl"), "w")
    triples = []
    for filename in os.listdir(input_dir):
        if filename.endswith("-train-translated.jsonl"):
            triples += create_triples(os.path.join(input_dir, filename), os.path.join(input_dir, filename.replace("-train-translated.jsonl", "-train-neg.json")), removed_queries)
    
    #shuffle triples
    random.shuffle(triples)

    for triple in triples:
        triples_file.write(json.dumps(triple) + "\n")
    print(">> Created a total of {n} triples".format(n=len(triples)))
    
def merge_queries_files(dir, output_filepath):
    '''
    dir: directory that contains all queries corpuses need to be merged into one large corpus
    '''
    queries = {}
    filenames = []
    removed_queries = set()
    for filename in os.listdir(dir):
        if filename.startswith("queries") and filename.endswith("-train.jsonl"):
            filenames.append(filename)
            data_filepath = os.path.join(dir, filename)
            with open(data_filepath) as file:
                reader = jsonlines.Reader(file)
                for line in reader:
                    if line["query_id"] in queries and queries[line["query_id"]] != line["query"]:
                        print("Warning: Duplicated queries, query: {query}, query_id: {query_id}".format(query=line["query"], query_id=line["query_id"]))
                    queries[line["query_id"]] = line["query"]
    
    with open(output_filepath, "w") as output_data_file:
        for id, query in queries.items():
            query = query.replace("\n","")
            if query and not query.isspace():
                output_data_file.write("{id}\t{data}\n".format(id = id, data = query))
            else:
                removed_queries.add(id)
    
    print("Merged query files: {files}".format(files = filenames))
    print("Saved to: {path}".format(path = output_filepath))

    return removed_queries

def jsonl_to_tsv(data_filepath, output_data_filepath):
    """
    Convert JSONL file with format {id:_,data:_} to TSV file with format id\tdata
    """
    output_data_file = open(output_data_filepath,"w")
    with open(data_filepath, "r") as data_file:
        reader = jsonlines.Reader(data_file)
        for line in reader:
            for key, value in line.items():
                if key.endswith("_id"):
                    id = value
                else:
                    val = value.replace("\n","")
            if val and not val.isspace():
                output_data_file.write("{id}\t{data}\n".format(id = id, data = val))
    output_data_file.close()
    print("Converted {file} to {output_file}".format(file = data_filepath, output_file = output_data_filepath))


def main():
    
    PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
    TRAINING_DATA_DIR = os.getenv('TRAINING_DATA_DIR')
    removed_queries = merge_queries_files(dir = PROCESSED_DATA_DIR, output_filepath = os.path.join(TRAINING_DATA_DIR,"queries.tsv"))

    jsonl_to_tsv(os.path.join(PROCESSED_DATA_DIR,"contexts-train.jsonl"), os.path.join(TRAINING_DATA_DIR,"contexts.tsv"))

    create_all_triples(output_dir=TRAINING_DATA_DIR, input_dir=PROCESSED_DATA_DIR, removed_queries=removed_queries)

if __name__=="__main__":
    main()
