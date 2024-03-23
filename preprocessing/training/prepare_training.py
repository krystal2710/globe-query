import jsonlines
import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('ROOT_DIR'))

def create_triples(data_filepath, data_neg_filepath, triples_filepath = os.getenv("TRAINING_TRIPLES_PATH")):
    print("Creating triples from {data_filepath} and {data_neg_filepath}".format(data_filepath = data_filepath, data_neg_filepath = data_neg_filepath))
    #Read the query-context jsonl file
    with open(data_filepath, "r") as data_file:
        reader = jsonlines.Reader(data_file)
        data = []
        for line in reader:
            data.append(line)
        
    #Read the query-negative context file
    with open(data_neg_filepath, "r") as data_neg_file:
        data_neg = {}
        json_raw = json.load(data_neg_file)["data"]
        for line in json_raw:
            if line["query_id"] not in data_neg:
                data_neg[line["query_id"]] = []
            data_neg[line["query_id"]].append(line["context_id"])
    
    #Open triples file
    triples_file = open(triples_filepath, "a")

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
        else:
            #iterate through each negative context
            for neg_pid in neg_pid_list:
                triple = [qid, pos_pid, neg_pid]
                triples_file.write(json.dumps(triple) + "\n")
                count_triples += 1

    triples_file.close()
    print("Created {i} triples".format(i = count_triples))
    print("There are {i}/{total} not found queries".format(i=count_not_found, total=n))


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

def create_all_triples():
    create_triples("data/processed/squad-train-translated.jsonl", "data/processed/squad-train-neg.json")
    create_triples("data/processed/korquad-train-translated.jsonl", "data/processed/korquad-train-neg.json")
    create_triples("data/processed/fquad-train-translated.jsonl", "data/processed/fquad-train-neg.json")
    create_triples("data/processed/uitviquad-train-translated.jsonl", "data/processed/uitviquad-train-neg.json")
    create_triples("data/processed/germanquad-train-translated.jsonl", "data/processed/germanquad-train-neg.json")

def convert_queries_and_contexts():
    jsonl_to_tsv(os.getenv("QUERIES_PATH"), os.getenv("TRAINING_QUERIES_PATH"))
    jsonl_to_tsv(os.getenv("CONTEXTS_PATH"), os.getenv("TRAINING_CONTEXTS_PATH"))

def main():
    convert_queries_and_contexts()
    create_all_triples()

if __name__=="__main__":
    main()
