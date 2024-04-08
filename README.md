# Multilingual Efficient and Effective Passage Search
## Brief Description
The evolution of Information Retrieval (IR) over the past decade has been significantly influenced by the integration of neural network models, shifting the focus from traditional term-based approaches to more nuanced semantic understanding. However, these advancements come at the cost of increased computational demands during both model training and query processing. The ColBERT model introduces an innovative "late interaction" architecture, optimizing the balance between semantic understanding and computational efficiency by encoding queries and documents into bags of embeddings before a computationally inexpensive "late interaction" step. Nevertheless, ColBERT's reliance on a monolingual BERT model limits its applicability to queries and documents in the same language, underscoring the need for multilingual capabilities in IR systems. Our study extends the ColBERT framework into the multilingual domain, exploring the construction of a multilingual dataset and the adaptation of ColBERT for efficient and accurate information retrieval across languages. The results show that while mColBERT is adept at sourcing relevant information in a multilingual setting, it shows a strong preference for delivering results within the same language of the query (monolingual search) rather than across languages (crosslingual search). In addition, mColBERT and mBART-50-m2m shows a slightly superior performance in terms of accuracy and relevance of response for queries in a high-resource language like English compared to a low-resource language like Korean, Vietnamese, French

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