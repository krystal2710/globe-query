import sys
import os
import argparse

from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('ROOT_DIR'))

from services.convert_data import convert_quad
            
def main():

    RAW_DATA_DIR = os.getenv('RAW_DATA_DIR')
    PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
    PROCESSED_TRAINING_CONTEXTS_PATH= "{dir}/contexts-train.jsonl".format(dir=PROCESSED_DATA_DIR)
    PROCESSED_TRAINING_QUERIES_PATH= "{dir}/queries-train.jsonl".format(dir=PROCESSED_DATA_DIR)

    #Parse argument for preprocessing each Question Answering Dataset. Args: data (str): Raw dataset name, e.g. squad-train, korquad-train, fquad-train
    parser = argparse.ArgumentParser(description='Preprocess each Question Answering Dataset')
    parser.add_argument('--data', help='raw dataset name, e.g. squad-train, korquad-train, fquad-train')
    args = parser.parse_args()

    #convert datasets from hierarchical model to relational model (tabular format)
    RAW_DATA_PATH = "{dir}/{data}-train.json".format(dir=RAW_DATA_DIR, data=args.data)
    TABULAR_DATA_PATH =  "{dir}/{data}-train.json".format(dir=PROCESSED_DATA_DIR, data=args.data)
    convert_quad(RAW_DATA_PATH, TABULAR_DATA_PATH, PROCESSED_TRAINING_CONTEXTS_PATH, PROCESSED_TRAINING_QUERIES_PATH, args.data)

if __name__ == '__main__':
    main()