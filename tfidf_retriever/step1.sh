export PYTHONPATH="${PYTHONPATH}:src/step1/DrQA"
DATASET_PATH="data/SQuAD/original/squad_train.json"
SAVE_PATH="data/SQuAD/adversarial/squad_train_step2.json"

python src/step1/main.py \
    --dataset_path ${DATASET_PATH} \
    --save_path ${SAVE_PATH} \
    --top_k 10 \
    --gt_score False \
    --num_unanswerable 43799

# The final database of all unans_candidates is saved at 
# retriever_component/unans_cdd/squad_train_unans_cdd.json