import json
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

def convert_quad(input_filename, output_filename, contexts_filename = os.getenv("CONTEXTS_PATH"), queries_filename = os.getenv("QUERIES_PATH")):
    """
    Convert hierarchical data in input_filename to tabular data and save it to output_filename.
    """ 
    
    # Load the data from the input file
    with open(input_filename) as input_file:
        data = json.load(input_file)
        if "data" in data:
            data = data["data"]

    # Open the context and query files to append new contexts and queries
    contexts = open(contexts_filename, 'a')
    queries = open(queries_filename, 'a')

    res = []
    for article in data:
        for p in article["paragraphs"]:

            #add new context to context file
            context_id = str(uuid.uuid4())
            new_context = {"context_id": context_id, "context": p["context"]}
            contexts.write(json.dumps(new_context) + "\n")

            for qas in p["qas"]:
                if not qas["answers"]:
                    continue
                
                #add new query to query file
                query_id = str(uuid.uuid4())
                new_query = {"query_id": query_id, "query": qas["question"]}
                queries.write(json.dumps(new_query) + "\n")
                
                #add new row to processed data
                curr_row = {"context_id": context_id, "query_id": query_id}
                res.append(curr_row)
    
    print("Completed conversion of {input_filename}".format(input_filename=input_filename))

    with open(output_filename, 'w') as output_file:
        json.dump(res, output_file)
    
    print("Saved to {output_filename}".format(output_filename=output_filename))

    print("Added new contexts and queries to {contexts_filename} and {queries_filename}".format(contexts_filename=contexts_filename, queries_filename=queries_filename))
