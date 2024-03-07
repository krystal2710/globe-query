import json
import argparse
import os
from retriever_tfidf import ranker_pipeline
from unans_cdd import convert_and_validate
from combine import combine, info


# A class to store all the Path to the TF-IDF component and Info about the dataset
class PATHS:
    # Current directory
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))

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

    parser = argparse.ArgumentParser(description='Extract Unanswerable Questions using predictions')
    parser.add_argument('--dataset_path', help='path/to/orriginal/dataset_name.json')
    parser.add_argument('--save_path', help='path/to/save/dataset_name_combine.json')
    parser.add_argument('--top_k', default=10, help='number_of_rank')
    parser.add_argument('--gt_score', default=False, help='ground_truth_score')
    parser.add_argument('--num_unanswerable', type=int, help='Number of Unanswerable Questions')
    args = parser.parse_args()


    # Store the information of the dataset to the class
    PATHS.DATA['dataset_path'] = args.dataset_path
    PATHS.DATA['dataset_name'] = os.path.basename(args.dataset_path).split(".")[0]
    PATHS.DATA['save_path'] = args.save_path

    # 1
    # Retrieve top k contexts
    ranker_pipeline(int(args.top_k), True if args.gt_score == 'True' else False, PATHS)

    if args.gt_score != "True":
        # 2
        # Convert top k from tfidf format to EQA format -> unanswerable candidates
        relevant_dataset_path = PATHS.TFIDF_PATH['relevant'] + PATHS.DATA['dataset_name'] + "_relevant.json"
        unans_candidates_path = PATHS.TFIDF_PATH['unans_cdd'] + PATHS.DATA['dataset_name'] + "_cdd.json"
        convert_and_validate(relevant_dataset_path, PATHS.DATA['save_path'], PATHS.DATA['dataset_path'])

