import json
import uuid

from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.append(os.getenv('ROOT_DIR'))

from services.jsonl import read_contexts
from services.jsonl import read_queries

def translate_text(target: str, text: str) -> dict:
    """
    Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]
    
def translate_all(input_filename, input_lang, output_filename, output_lang_lists, progress_env_name):
    """
    Translates the queries in the input file from the input language to multiple output languages and saves to an output file.
    """
    progress = int(os.getenv(progress_env_name))
    print("Translating {input_filename} from row {progress}".format(input_filename=input_filename, progress=progress))

    #Read the input and output file
    with open(input_filename) as input_file:
        data = json.load(input_file)
    output_file = open(output_filename, 'w')
    
    #Read the context and query files
    contexts = read_contexts(os.getenv("CONTEXTS_PATH"))
    queries = read_queries(os.getenv("QUERIES_PATH"))
    queries_file = open(os.getenv("QUERIES_PATH"), 'a')

    for i in range(progress, len(data)):
        row = data[i]

        #Add the original query-context pair to the output file
        original_row = {"context_id": row["context_id"], "query_id": row["query_id"], "orig_query_id": row["query_id"],"context_lang":input_lang, "query_lang":input_lang}
        output_file.write(json.dumps(original_row) + "\n")

        for output_lang in output_lang_lists:
            try:
                query = queries[row["query_id"]]

                #Translate the query and add new query to query file
                translated_query = translate_text(output_lang, query)
                query_id = str(uuid.uuid4())
                queries_file.write(json.dumps({"query_id": query_id, "query": translated_query}) + "\n")

                #Add translated query-context pair to the output file
                new_row = {"context_id":row["context_id"], "query_id": query_id, "orig_query_id": row["query_id"], "context_lang":input_lang, "query_lang":output_lang}
                output_file.write(json.dumps(new_row) + "\n")

            except:
                print("Error translating row {i} with qid {qid}".format(i=i, qid=row["query_id"]))
                # Read the .env file
                with open('.env', 'r') as f:
                    lines = f.readlines()

                # Modify the variable's value
                new_lines = []
                changed_line = "{MY_VARIABLE}=".format(MY_VARIABLE=progress_env_name)
                for line in lines:
                    if line.startswith(changed_line):
                        line = changed_line + str(i) + "\n"
                    new_lines.append(line)

                # Write the .env file
                with open('.env', 'w') as f:
                    f.writelines(new_lines)

        if i % 10 == 0:
            print("Translated {i} rows".format(i=i))

    print("Translated a total of {i} rows".format(i=i))
    #Close the files
    output_file.close()
    queries_file.close()

    print("Saved to {output_filename}\n".format(output_filename=output_filename))
