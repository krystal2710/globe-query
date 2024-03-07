import json
import argparse
import os
import jsonlines
from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.append(os.getenv('ROOT_DIR'))

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
    with jsonlines.open(os.getenv("CONTEXTS_PATH")) as reader:
        for line in reader:
            context_search[line["context"]] = line["context_id"]

    #Read the queries file
    query_search = {}
    with jsonlines.open(os.getenv("QUERIES_PATH")) as reader:
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



# Check if any raw_tfidf context is mixed in the ground_truth ==================================================================================
def check_dataset(unans_candidates_path, dataset_path):

    unans_cand_data = read_dataset(unans_candidates_path)['data']
    ans_data = read_dataset(dataset_path)['data']

    # Comparing two dataset
    ans_dict = {} # the dictionary with key = question, value = [ground_truth]
    count_overlap = 0
    count_ques = 0
    count_tfidf = 0

    for item in ans_data:
        context = item['context']
        ques = item['question'] 
        count_ques += 1        
        if ques in ans_dict.keys():
            ans_dict[ques].append(context)
        else:
            ans_dict[ques] = [context]

    for item in unans_cand_data:
        context = item['context'] 
        count_tfidf += 1
        ques = item['question']
        if context in ans_dict[ques]: # check if there is any ground truth in the unans_candidate
            count_overlap += 1

    #PRINT THE COUNT
    print("Unanswerable candidates info:")
    print("Overlap:", count_overlap)
    print("# of original ques:", count_ques)
    print("# of unanswerable candidate question:", count_tfidf, "\n")


# ========================================================================================================================
# MAIN ===================================================================================================================

def convert_and_validate(relevant_dataset_path, unans_candidates_path, dataset_path):
    tfidf2eqa(relevant_dataset_path, unans_candidates_path)
    # check_dataset(unans_candidates_path, dataset_path)
