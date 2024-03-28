import os
import sys

from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('ROOT_DIR'))

PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
TRAINING_INPUT_DATA_DIR = os.getenv('TRAINING_INPUT_DATA_DIR')
PROCESSED_TRAINING_CONTEXTS_PATH= "{dir}/contexts-train.jsonl".format(dir=PROCESSED_DATA_DIR)
PROCESSED_TRAINING_QUERIES_PATH= "{dir}/queries-train.jsonl".format(dir=PROCESSED_DATA_DIR)

def create_context_and_query_files(contexts_filename = PROCESSED_TRAINING_CONTEXTS_PATH, queries_filename = PROCESSED_TRAINING_QUERIES_PATH):

    if not os.path.exists(contexts_filename):
        with open(contexts_filename, "w") as f:
            # Create an empty JSONL file
            f.write("")
        print("Created contexts file at {filename}".format(filename=contexts_filename))

    if not os.path.exists(queries_filename):
        with open(queries_filename, "w") as f:
            # Create an empty JSONL file
            f.write("")
        
        print("Created queries file at {filename}".format(filename=queries_filename))

def main():

    #create data directories
    if not os.path.exists(PROCESSED_DATA_DIR):
        os.system("mkdir {dir}".format(dir=PROCESSED_DATA_DIR))

    if not os.path.exists(TRAINING_INPUT_DATA_DIR):
        os.system("mkdir {dir}".format(dir=TRAINING_INPUT_DATA_DIR))

    #check for context and query file, create if not exist
    create_context_and_query_files()

if __name__ == "__main__":
    main()