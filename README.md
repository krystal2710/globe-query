# Crosslingual Efficient and Effective Passage Search
## Brief Description
The purpose of the study is to develop mColBERT (Multilingual ColBERT), a cross-lingual search engine capable of effectively retrieving information across multiple languages. That is, given a query in one language, the search engine is capable of finding relevant contexts in other languages, effectively overcoming the challenges of language barriers in information retrieval.

Additionally, this research explores the effectiveness of mColBERT across different languages and investigates the factors contributing to performance variations. Furthermore, the research aims to un- derstand the curse of multilinguality, of which pre-trained multilingual models often show many language weaknesses compared to monolingual counterparts in monolingual settings. To investigate this, the research evaluates the performance of ColBERT and mColBERT on same-language open-domain QA tasks.

## Author information and contact
- Krystal Ly
- krystally2710@gmail.com

## Data

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
  ROOT_DIR="path/to/root/directory"
  QUERIES_PATH="path/to/queries.jsonl"   #queries.jsonl is used throughout Step 2a
  CONTEXTS_PATH="path/to/contexts.jsonl" #contexts.jsonl is used throughout Step 2b
  TRAINING_QUERIES_PATH="path/to/training_queries.tsv"  #queries.tsv is used as training input
  TRAINING_CONTEXTS_PATH="path/to/training_contexts.tsv" #contexts.tsv is used as training input
  TRAINING_TRIPLES_PATH="path/to/training_triples.tsv"
  COLBERT_PATH="path/to/colbert_model"
  ```
Step 2a: Preprocess the data
  ```sh
  python3 preprocessing/training/preprocess_data.py
  ```

Step 2b: Run TF-IDF retriever to retrieve negative passages
  ```sh
  bash tfidf_retriever/run_retriever.sh
  ```

Step 3: Start training
  ```sh
  python3 training/training.py
  ```
