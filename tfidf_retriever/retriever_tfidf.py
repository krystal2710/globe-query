from DrQA.drqa import retriever
import json
import argparse
import os
# from PATH import TFIDF_PATH, CURR_DIR
import jsonlines
from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.append(os.getenv('ROOT_DIR'))

PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
PROCESSED_TRAINING_CONTEXTS_PATH= "{dir}/contexts_train.jsonl".format(dir=PROCESSED_DATA_DIR)
PROCESSED_TRAINING_QUERIES_PATH= "{dir}/queries_train.jsonl".format(dir=PROCESSED_DATA_DIR)

# RETRIEVE THE CURRENT DIRECTORY =====================================================================================================

def read_dataset(path):
    f = open(path, "r")
    dataset = json.load(f)
    return dataset

def write_output(path_save, data):
    if not os.path.exists(path_save):
        os.mknod(path_save)
    # Write the combined dataset to a JSON file
    with open(path_save, 'w') as f:
        json.dump(data, f, indent=4)


# CONVERT THE JSON FILE INTO DRQA FORM ==============================================================================================
def prepare_db(dataset_name, PATHS):
    """
    Input: the orginal dataset in EQA format + the name of the data (this will be used as the main name for the TFIDF process)
    Output: db_format dataset for creating database + 2 dictionary of contexts and questions
    
    Format: -------------------
    contexts = {
        "1": context1,
        "2": context2,
        ...
    }

    questions = {
        question1: [context1, context2, ....],
        ...
    }
    ---------------------------
    
    The `questions` dict will be use in the last step: create a loop to find the tfidf rank of each question in the dictionary keys
    The contexts in the `questions` dict are the ground truth of the questions
    """

    # Read the dataset from json ---------------------
    data = read_dataset(PATHS.DATA["dataset_path"])

    #Read the contexts file
    context_search = {}
    with jsonlines.open(PROCESSED_TRAINING_CONTEXTS_PATH) as reader:
        for line in reader:
            context_search[line["context_id"]] = line["context"]

    #Read the queries file
    query_search = {}
    with jsonlines.open(PROCESSED_TRAINING_QUERIES_PATH) as reader:
        for line in reader:
            query_search[line["query_id"]] = line["query"]

    # Create dataset in db_form and prepare ground truth context for each questions ---------------------
    ques_dict, context_dict = {}, {}
    contexts_set = set()
    db_form = []

    # this is used as the index of the context, which will 
    # be used to pull out to check the tfidf individually if needed
    count = 0  
    
    for item in data:
        context = context_search[item["context_id"]]

        # If the context is not added
        if context not in contexts_set: 
            # Add context into db_form for retrieving
            db_form.append({"id": str(count), "text": context}) # db format

            # Add new context found to the contexts dictionary
            context_dict[str(count)] = context
            
            count += 1 # increase the ID

        # add context to the set
        contexts_set.add(context)
        
        # Add question and corresponding ground truth context
        ques = query_search[item['query_id']]
        if ques in ques_dict.keys():
            ques_dict[ques].add(context)
        else:
            ques_dict[ques] = set()
            ques_dict[ques].add(context)


    # Create destination for db_form dataset ---------------------
    db_form_path = PATHS.TFIDF_PATH["db_form"] + dataset_name + "_db_form.json"
    save_folder = os.path.dirname(db_form_path)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    outfile = open(db_form_path, "w")
    
    # Write output
    for i in db_form:
        outfile.write(json.dumps(i) + '\n')


    return (db_form_path, (ques_dict, context_dict))




# CONVERT THE TFIDF_form.JSON FORM INTO .DB DATABASE =============================================================================================
def convert_to_db(db_form_path, PATHS):
    db_path = PATHS.TFIDF_PATH["db_path"] + PATHS.DATA["dataset_name"] + ".db" # create path to save the database
    db_buider_PATH = PATHS.CURR_DIR + "/DrQA/scripts/retriever/build_db.py"           # evoke the db builder python file
    
    command = "python " + db_buider_PATH + " " + db_form_path + " " + db_path   # the command for the db builder
    os.system(command)

    return db_path




# CREATE THE TFIDF RANKER FORM THE DATABASE .DB INTO TFIDF RANKER ==========================================================================
def build_tfidf(db_path, PATHS):
    tfidf_folder_path = PATHS.TFIDF_PATH['tfidf_folder_path']                  # path to save the tfidf ranker
    tfidf_buider_PATH = PATHS.CURR_DIR + "/DrQA/scripts/retriever/build_tfidf.py"     # evoke the drqa tfidf builder python file

    command = "python " + tfidf_buider_PATH + " " + db_path + " " + tfidf_folder_path   # the command for the tfidf builder
    os.system(command)

    tfidf_path = tfidf_folder_path + "/" + PATHS.DATA["dataset_name"] + "-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz" # return the path to the ranker
    return tfidf_path




# USING THE TFIDF RANKER TO CREATE A JSON RANKING FILE  ==================================================================================
def rank_doc(ranker, ques_dict, context_dict, PATHS, top_k=10, ground_truth_score=False):
    
    # tf-idf file
    tfidf_pairs = {'documents': []} 

    # Use to calculate the score of the ground_truth
    reverse_contexts = {k: v for v, k in context_dict.items()}
    ground_truth = {}
    
    # This will be used to log the status of the TFIDF process
    total_ques = len(ques_dict)
    num_ques = 0

    # for each question as the key of the ques_dict dict, we look up for its tfidf
    for ques, texts in ques_dict.items():
            
        if ground_truth_score != True:
            relevant = [] # tf-idf context of the question

            doc_id, doc_scores, doc_texts = ranker.closest_docs(ques, k = top_k+5) # get the most 10 relevant context

            # Select each relevant context such that
            # <10 relevant text && the context is not ground_truth && the context is not duplicated
            for i in range(len(doc_id)):
                if (len(relevant) < top_k) and (context_dict[doc_id[i]] not in ques_dict[ques]) and (context_dict[doc_id[i]] not in relevant):
                    relevant.append(context_dict[ doc_id[i] ])

            # Add to the table all the relevant context found
            for item in relevant:
                tfidf_pairs['documents'].append({
                    "question" : ques,
                    "context": item
                })

        # -------- Code to score GROUND_TRUTH ---------------
        else:
            index_ground_truth = list(map(lambda x: reverse_contexts[x], ques_dict[ques]))

            for i in range(len(index_ground_truth)):
                doc_id_gt, doc_scores_gt, doc_texts_gt = ranker.closest_docs(ques, k=1, index_ques=index_ground_truth[i])
                if ques not in ground_truth.keys():
                    ground_truth[ques] = []
                ground_truth[ques].append([context_dict[doc_id_gt[0]], 0 if len(doc_scores_gt.tolist()) == 0 else doc_scores_gt.tolist()[0]])

        # Logging the status of the process
        num_ques += 1
        if num_ques % 500 == 0:
            print("Proccessing:", num_ques, "/", total_ques)

    # Writing to sample.json
    if ground_truth_score != True:
        write_output(PATHS.TFIDF_PATH["relevant"] + PATHS.DATA["dataset_name"] + "_relevant.json", tfidf_pairs)
    else:
        write_output(PATHS.TFIDF_PATH["gt_score"] + PATHS.DATA["dataset_name"] + "_gt_score.json", ground_truth)


# ========================================================================================================================
# PIPELINE ===============================================================================================================
# ========================================================================================================================
def ranker_pipeline(top_k, gt_score, PATHS):
    dataset_path = PATHS.DATA["dataset_path"]
    dataset_name = PATHS.DATA["dataset_name"]


    # CONVERTING TO DRQA DATASETS
    print("CONVERTING TO TFIDF DATASETS =======================================================")
    db_form_path, (ques_dict, context_dict) = prepare_db(dataset_name, PATHS)
    print(" **** Dataset ready:", db_form_path, " **** \n")

    # # CONVERTING TO DATABASE
    print("CONVERTING TO DATABASE =======================================================")
    db_path = convert_to_db(db_form_path, PATHS)
    print(" **** Database ready:", db_path, " **** \n")

    # # PREPATING TFIDF RANKER
    print("PREPARING TFIDF RANKER ========================================================")
    tfidf_path = build_tfidf(db_path, PATHS)
    ranker = retriever.get_class('tfidf')(db_path=db_path, tfidf_path=tfidf_path)
    print(" **** TFIDF ready:", tfidf_path, " **** \n")
    
    # RANKING THE ORIGINAL DOCUMENT
    print("RANKING THE ORIGINAL DOCUMENT ========================================================")
    rank_doc(ranker, ques_dict, context_dict, PATHS, top_k, gt_score)
    print("success!\n")

