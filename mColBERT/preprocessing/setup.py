import os
import sys

from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('ROOT_DIR'))

PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
TRAINING_DATA_DIR = os.getenv('TRAINING_DATA_DIR')
PROCESSED_TRAINING_CONTEXTS_PATH = os.path.join(PROCESSED_DATA_DIR,"contexts-train.jsonl")
PROCESSED_TRAINING_QUERIES_PATH = os.path.join(PROCESSED_DATA_DIR,"queries-train.jsonl")

def create_context_and_query_files(contexts_filename = PROCESSED_TRAINING_CONTEXTS_PATH, queries_filename = PROCESSED_TRAINING_QUERIES_PATH):

    with open(contexts_filename, "w") as f:
        # Create an empty JSONL file
        f.write("")
    print("---Created contexts file at {filename}".format(filename=contexts_filename))

    with open(queries_filename, "w") as f:
        # Create an empty JSONL file
        f.write("")
    
    print("---Created queries file at {filename}".format(filename=queries_filename))

def main():

    #create data directories or delete previous training files
    if not os.path.exists(PROCESSED_DATA_DIR):
        os.system("mkdir {dir}".format(dir=PROCESSED_DATA_DIR))
    else:
        print(">> Starting delete existing files in processed folder")
        print()
        for filename in os.listdir(PROCESSED_DATA_DIR):
            if filename.endswith("-train-translated.jsonl") or filename.endswith("-train-neg.json") or filename.endswith("-train.json"):
                os.system("rm -f {file}".format(file = os.path.join(PROCESSED_DATA_DIR, filename)))

    if not os.path.exists(TRAINING_DATA_DIR):
        os.system("mkdir {dir}".format(dir=TRAINING_DATA_DIR))

    else:
        print(">> Starting delete existing files in training input folder")
        print()
        for filename in os.listdir(TRAINING_DATA_DIR):
            os.system("rm -f {file}".format(file = os.path.join(TRAINING_DATA_DIR, filename)))

    #check for context and query file, create if not exist
    create_context_and_query_files()

if __name__ == "__main__":
    main()