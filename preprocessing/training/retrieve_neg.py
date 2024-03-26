import json
import argparse
import os
import sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('TFIDF_RETRIEVER_DIR'))
os.environ["PYTHONPATH"] = "${PYTHONPATH}:tfidf_retriever/DrQA"
from retriever_tfidf import ranker_pipeline
from unans_cdd import convert_and_validate


# A class to store all the Path to the TF-IDF component and Info about the dataset
class PATHS:
    # Current directory
    CURR_DIR = os.getenv('TFIDF_RETRIEVER_DIR')

    # TF-IDF component
    TFIDF_PATH = {
        "db_form":              CURR_DIR + "/retriever_component/db_form/",
        "db_path":              CURR_DIR + "/retriever_component/SQLdatabase/",
        "tfidf_folder_path":    CURR_DIR + "/retriever_component/tfidf",
        "relevant":             CURR_DIR + "/retriever_component/tfidf_data/relevant/",
        "gt_score":             CURR_DIR + "/retriever_component/tfidf_data/gt_score/",
        "unans_cdd":            CURR_DIR + "/retriever_component/unans_cdd/"
    }

    # Data info
    DATA = {
        "dataset_name": "",
        "dataset_path": "",
        "save_path": ""
    }

if __name__ == '__main__':

    os.system("export PYTHONPATH=${PYTHONPATH}:tfidf_retriever/DrQA")
    PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
    parser = argparse.ArgumentParser(description='Retrieve negative contexts for given queries')
    parser.add_argument('--data', help='dataset name, e.g. squad-train, korquad-train, fquad-train')
    parser.add_argument('--top_k', default=5, help='number_of_rank')
    parser.add_argument('--gt_score', default=False, help='ground_truth_score')
    parser.add_argument('--num_unanswerable', default=43799,type=int, help='Number of Unanswerable Questions')
    args = parser.parse_args()


    # Store the information of the dataset to the class
    PATHS.DATA['dataset_path'] = "{dir}/{data}.json".format(dir=PROCESSED_DATA_DIR, data=args.data)
    PATHS.DATA['dataset_name'] = args.data
    PATHS.DATA['save_path'] = "{dir}/{data}-neg.json".format(dir=PROCESSED_DATA_DIR, data=args.data)

    # 1
    # Retrieve top k contexts
    ranker_pipeline(int(args.top_k), True if args.gt_score == 'True' else False, PATHS)

    if args.gt_score != "True":
        # 2
        # Convert top k from tfidf format to EQA format -> unanswerable candidates
        relevant_dataset_path = PATHS.TFIDF_PATH['relevant'] + PATHS.DATA['dataset_name'] + "_relevant.json"
        unans_candidates_path = PATHS.TFIDF_PATH['unans_cdd'] + PATHS.DATA['dataset_name'] + "_cdd.json"
        convert_and_validate(relevant_dataset_path, PATHS.DATA['save_path'])

