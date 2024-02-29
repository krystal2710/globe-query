import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv('ROOT_DIR'))

from services.convert_data import convert_quad
from services.convert_data import convert_cmrc
from services.translate_queries import translate_all

ALL_LANGUAGES = ["en", "de", "ko", "fr", "vi", "zh"]

def convert_all_quads():
    convert_quad("data/raw/squad-train-v1.1.json", "data/processed/squad-train-v1.1.json")
    convert_quad("data/raw/korquad-train-v1.0.json", "data/processed/korquad-train-v1.0.json")
    convert_quad("data/raw/germanquad-train.json", "data/processed/germanquad-train.json")
    convert_quad("data/raw/fquad-train.json", "data/processed/fquad-train.json")
    convert_quad("data/raw/uitviquad-train.json", "data/processed/uitviquad-train.json")
    convert_cmrc("data/raw/cmrc-train-v2018.json", "data/processed/cmrc-train-v2018.json")

def translate_all_data():
    translate_all("data/processed/squad-train-v1.1.json", "en", "data/processed/squad-train-translated.json", ALL_LANGUAGES[1:])
    translate_all("data/processed/germanquad-train.json", "de", "data/processed/germanquad-train-translated.json", ALL_LANGUAGES[0] + ALL_LANGUAGES[2:])
    translate_all("data/processed/korquad-train-v1.0.json", "ko", "data/processed/korquad-train-translated.json", ALL_LANGUAGES[0:2]+ALL_LANGUAGES[3:])
    translate_all("data/processed/fquad-train.json", "fr", "data/processed/fquad-train-translated.json", ALL_LANGUAGES[0:3]+ALL_LANGUAGES[4:])
    translate_all("data/processed/uitviquad-train.json", "vi", "data/processed/uitviquad-train-translated.json", ALL_LANGUAGES[0:4]+ALL_LANGUAGES[5:])
    translate_all("data/processed/cmrc-train-v2018.json", "zh", "data/processed/cmrc-train-translated.json", ALL_LANGUAGES[0:5])
                  
def main():

    #convert datasets from hierarchical model to relational model (tabular format)
    convert_all_quads()

    #translate all queries from one language to all other languages and save to new files
    translate_all_data()

if __name__ == '__main__':
    main()