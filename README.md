# Multilingual Efficient and Effective Passage Search
## Brief Description
The purpose of the study is to develop mColBERT (Multilingual ColBERT), a cross-lingual search engine capable of effectively retrieving information across multiple languages. That is, given a query in one language, the search engine is capable of finding relevant contexts in other languages, effectively overcoming the challenges of language barriers in information retrieval.

Additionally, this research explores the effectiveness of mColBERT across different languages and investigates the factors contributing to performance variations. Furthermore, the research aims to un- derstand the curse of multilinguality, of which pre-trained multilingual models often show many language weaknesses compared to monolingual counterparts in monolingual settings. To investigate this, the research evaluates the performance of ColBERT and mColBERT on same-language open-domain QA tasks.

## Author information and contact
- Krystal Ly
- krystally2710@gmail.com

## Data
The study uses SQuAD, KorQuAD, UIT-ViQuAD, GermanQuAD, FQuAD as foundational data. Download the data at https://huggingface.co/datasets/krystal2710/mColBERT-data

## Get Started
Create a virtual environment
  ```sh
  pip install virtualenv
  python3 -m venv env
  ```

Activate the virtual environment
  ```sh
  source env/bin/activate
  ```

Run the following commands in the terminal to install required packages
  ```sh
  pip install -r requirements.txt
  ```
## Reproduce
Reproducing the study involves the following steps:

Step 1: Create .env
  ```sh
  ROOT_DIR=path/to/root/directory
  RAW_DATA_DIR=path/to/data/raw/directory
  PROCESSED_DATA_DIR=path/to/data/processed/directory
  TRAINING_DATA_DIR=path/to/training_data/directory
  TESTING_DATA_DIR=path/to/testing_data/directory
  TFIDF_RETRIEVER_DIR=path/to/tfidf_retriever/directory
  COLBERT_PATH=path/to/colbert/directory
  ```

Step 2: Download the data at https://huggingface.co/datasets/krystal2710/mColBERT-data

Step 3: Preprocess the data
  ```sh
  python3 preprocessing/setup.py
  python3 preprocessing/preprocess_data.py --data [data_name] #data_name should be squad, korquad, fquad, etc. Run for each separately
  ```

Step 4: Translate 
  ```sh
  python3 preprocessing/translate_data.py --data [data_name] --lang [data_lang] #data_lang should en, ko, vi, fr, de. Run for each separately
  ```

Step 5: Run TF-IDF retriever to retrieve negative passages
  ```sh
  python3 preprocessing/retrieve_neg.py --data [data_name] #data_name should be squad, korquad, fquad, etc. Run for each separately
  ```

Step 6: Training
  ```sh
  python3 training/training.py
  ```

Step 7: Testing
  See `testing.ipynb`