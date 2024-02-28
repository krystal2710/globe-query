def main():
    import json
    import sys
    import os
    from dotenv import load_dotenv

    load_dotenv()
    sys.path.append(os.getenv('ROOT_DIR'))

    from services.convert_data import convert_quad
    from services.convert_data import convert_cmrc

    #convert datasets from hierarchical model to relational model (tabular format)
    convert_quad("data/raw/squad-train-v1.1.json", "data/processed/squad-train-v1.1.json")
    convert_quad("data/raw/korquad-train-v1.0.json", "data/processed/korquad-train-v1.0.json")
    convert_quad("data/raw/germanquad-train.json", "data/processed/germanquad-train.json")
    convert_quad("data/raw/fquad-train.json", "data/processed/fquad-train.json")
    convert_quad("data/raw/uitviquad-train.json", "data/processed/uitviquad-train.json")
    convert_cmrc("data/raw/cmrc-train-v2018.json", "data/processed/cmrc-train-v2018.json")

if __name__ == '__main__':
    main()