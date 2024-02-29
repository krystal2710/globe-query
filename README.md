# Crosslingual Efficient and Effective Passage Search
## Brief Description
The purpose of the study is to develop mColBERT (Multilingual ColBERT), a cross-lingual search engine capable of effectively retrieving information across multiple languages. That is, given a query in one language, the search engine is capable of finding relevant contexts in other languages, effectively overcoming the challenges of language barriers in information retrieval.

Additionally, this research explores the effectiveness of mColBERT across different languages and investigates the factors contributing to performance variations. Furthermore, the research aims to un- derstand the curse of multilinguality, of which pre-trained multilingual models often show many language weaknesses compared to monolingual counterparts in monolingual settings. To investigate this, the research evaluates the performance of ColBERT and mColBERT on same-language open-domain QA tasks.

## Author information and contact
- Krystal Ly
- krystally2710@gmail.com

## Data

## Getting Started
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
## Reproducibility
Reproducing the study involves the following steps:

Step 1: Preprocess the data
  ```sh
  python3 preprocessing/training/preprocess_data.py
  ```

## Code (what code files exist? What does each do? Is there an order needed to run them?)
