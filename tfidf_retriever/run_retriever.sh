export PYTHONPATH="${PYTHONPATH}:tfidf_retriever/DrQA"

python tfidf_retriever/main.py \
    --dataset_path data/processed/squad-train.json \
    --save_path data/processed/squad-train-neg.json \
    --top_k 5 \
    --gt_score False \
    --num_unanswerable 43799

python tfidf_retriever/main.py \
    --dataset_path data/processed/fquad-train.json \
    --save_path data/processed/fquad-train-neg.json \
    --top_k 5 \
    --gt_score False \
    --num_unanswerable 43799

python tfidf_retriever/main.py \
    --dataset_path data/processed/germanquad-train.json \
    --save_path data/processed/germanquad-train-neg.json \
    --top_k 5 \
    --gt_score False \
    --num_unanswerable 43799

python tfidf_retriever/main.py \
    --dataset_path data/processed/korquad-train.json \
    --save_path data/processed/korquad-train-neg.json \
    --top_k 5 \
    --gt_score False \
    --num_unanswerable 43799

python tfidf_retriever/main.py \
    --dataset_path data/processed/uitviquad-train.json \
    --save_path data/processed/uitviquad-train-neg.json \
    --top_k 5 \
    --gt_score False \
    --num_unanswerable 43799

# The final database of all unans_candidates is saved at 
# retriever_component/unans_cdd/squad_train_unans_cdd.json