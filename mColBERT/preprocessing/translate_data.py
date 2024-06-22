import sys
import os
import argparse

from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('ROOT_DIR'))

from services.translate_queries import translate_all
            
def main():

    PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
    PROCESSED_TRAINING_QUERIES_PATH = os.path.join(PROCESSED_DATA_DIR,"queries-train.jsonl")

    #Parse argument for preprocessing each Question Answering Dataset. Args: data (str): Raw dataset name, e.g. squad-train, korquad-train, fquad-train
    parser = argparse.ArgumentParser(description='Preprocess each Question Answering Dataset')
    parser.add_argument('--data', help='raw dataset name, e.g. squad-train, korquad-train, fquad-train')
    parser.add_argument('--lang', help='language code of raw dataset, e.g. en, de, ko')
    args = parser.parse_args()

    #translate all queries from one language to all other languages and save to new files
    TABULAR_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "{data}-train.json".format(data=args.data))
    TRANSLATED_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "{data}-train-translated.jsonl".format(data=args.data))
    TRANSLATED_LANGUAGES = [lang for lang in ["en", "de", "ko", "fr", "vi"] if lang != args.lang]

    # NOTE: uncomment this line if run code in paralell
    # OUTPUT_QUERIES_PATH = os.path.join(PROCESSED_DATA_DIR, "queries-{lang}-train.jsonl".format(lang = args.lang)) 
    translate_all(TABULAR_DATA_PATH, args.lang, TRANSLATED_DATA_PATH, TRANSLATED_LANGUAGES, PROCESSED_TRAINING_QUERIES_PATH, PROCESSED_TRAINING_QUERIES_PATH)

if __name__ == '__main__':
    main()