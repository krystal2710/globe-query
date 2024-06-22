# Step 1

Use command/step1.sh for step 1 ({dataset_name}_unans_cdd.json)

```
python src/step1/main.py \
    --dataset_path ${DATASET_PATH} \
    --save_path ${SAVE_PATH} \
    --top_k 10 \
    --gt_score False \
    --num_unanswerable 43799
```


`--dataset_path`: Path to the answerable dataset <br>
`--save_path`: Path to save the training file for adversarial models in step 2 <br>
`--top_k`: Number of context matched to each question using TF-IDF <br>
`--gt_score` (default = False): Parameter to print the score of the TF-IDF of answerable context - question <br>
`--num_unanswerable` (default = False): number of unanswerable candidates to combine with the answerable (original) dataset for step 2 <br>

The flow of the dataset in phase 1 is presented as follows: <br>
1. The dataset is parsed through the main.py file, then the information of the answerable dataset is retrieved <br>
2. The TF-IDF ranker is deployed:
    1. If the `--gt_score=True`, the ground truth score of the answerable dataset is saved under `retriever_component/tfidf_data/gt_score`
    2. If the `--gt_score=False`, we prepare the db form and database of the answerable dataset, then save it under `retriever_component/db_form` and `retriever_component/SQLdatabase` <br>
    3. Save top_k contexts under `retriever_component/tfidf_data/relevant`
3. The top_k context-question under `retriever_component/tfidf_data/relevant` is parsed through the `unans_cdd.py` file for re-formatting purposes. The final database of all unans_candidates is saved at `retriever_component/unans_cdd/`.
4. The combine.py file is used to combine the answerable datasets with `--num_unanswerable` of the unanswerable candidates dataset to prepare for phase 2.
