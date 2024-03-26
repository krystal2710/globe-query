import json
import argparse
import os
import jsonlines
from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.append(os.getenv('ROOT_DIR'))
PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
PROCESSED_TRAINING_CONTEXTS_PATH= "{dir}/contexts_train.jsonl".format(dir=PROCESSED_DATA_DIR)
PROCESSED_TRAINING_QUERIES_PATH= "{dir}/queries_train.jsonl".format(dir=PROCESSED_DATA_DIR)

# Read and write json file =====================================================================================
def read_dataset(path):
    f = open(path, "r")
    dataset = json.load(f)
    return dataset

def write_output(path_save, data):
    if not os.path.exists(path_save):
        os.mknod(path_save)
    # Write the combined dataset to a JSON file
    with open(path_save, 'w') as f:
        json.dump(data, f, indent=4)


# Convert TFIDF form into EQA form ======================================================================================
def tfidf2eqa(relevant_dataset_path, unans_candidates_path):
    dataset = read_dataset(relevant_dataset_path)
    data = dataset['documents']

    # question_id = 0
    dataset_format = {'data': []}

    #Read the contexts file
    context_search = {}
    with jsonlines.open(PROCESSED_TRAINING_CONTEXTS_PATH) as reader:
        for line in reader:
            context_search[line["context"]] = line["context_id"]

    #Read the queries file
    query_search = {}
    with jsonlines.open(PROCESSED_TRAINING_QUERIES_PATH) as reader:
        for line in reader:
            query_search[line["query"]] = line["query_id"]

    # Iterate through each question and context in the tfidf
    for i in range(len(data)):
        item = {}
        item['query_id'] = query_search[data[i]['question']]
        item['context_id'] = context_search[data[i]['context']]

        dataset_format['data'].append(item)
        # question_id += 1

    # Save the output
    write_output(unans_candidates_path, dataset_format)

# ========================================================================================================================
# MAIN ===================================================================================================================

def convert_and_validate(relevant_dataset_path, unans_candidates_path):
    tfidf2eqa(relevant_dataset_path, unans_candidates_path)
