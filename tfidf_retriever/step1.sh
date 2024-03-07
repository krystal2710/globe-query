export PYTHONPATH="${PYTHONPATH}:tfidf_retriever/DrQA"
DATASET_PATH="data/processed/uitviquad-train.json"
SAVE_PATH="data/processed/uitviquad-train-neg.json"

python tfidf_retriever/main.py \
    --dataset_path ${DATASET_PATH} \
    --save_path ${SAVE_PATH} \
    --top_k 5 \
    --gt_score False \
    --num_unanswerable 43799

# The final database of all unans_candidates is saved at 
# retriever_component/unans_cdd/squad_train_unans_cdd.json