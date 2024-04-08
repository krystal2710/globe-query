import json
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import jsonlines

from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.append(os.getenv('ROOT_DIR'))

from services.jsonl import read_contexts
from services.jsonl import read_queries


def translate_all(input_filename, input_lang, output_filename, output_lang_lists, input_queries_filepath, output_queries_filepath, batch_size=10):
    """
    Translates the queries in the input file from the input language to multiple output languages and saves to an output file.
    """
    lang_dict = {"en":"en_XX", "de":"de_DE", "ko":"ko_KR", "vi":"vi_VN", "fr":"fr_XX"}

    #Load translation model a.k.a mbart fine-tuned checkpt
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    model.cuda()
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    tokenizer.src_lang = lang_dict[input_lang]

    print("Translating {input_filename}".format(input_filename=input_filename))

    #Read the input and output file
    with open(input_filename) as input_file:
        data = json.load(input_file)
    output_file = open(output_filename, 'w')
    
    #Read the query files
    queries = {}
    queries_file = open(output_queries_filepath, 'w')

    with jsonlines.open(input_queries_filepath) as reader:
        for line in reader:
            queries[line["query_id"]] = line["query"]
            queries_file.write(json.dumps(line)+"\n")

    #Add the original query-context pair to the output file
    for row in data:
        original_row = {"context_id": row["context_id"], "query_id": row["query_id"], "orig_query_id": row["query_id"],"context_lang":input_lang, "query_lang":input_lang}
        output_file.write(json.dumps(original_row) + "\n")
    
    #Add the original query to the query file
    

    for output_lang in output_lang_lists:
        for start in range(0,len(data),batch_size):
            batch = [queries[data[i]["query_id"]] for i in range(start, min(start+batch_size,len(data)))]
            
            encoded_inputs = tokenizer(batch, return_tensors="pt", padding=True).to("cuda")
            generated_tokens = model.generate(
                **encoded_inputs,
                forced_bos_token_id=tokenizer.lang_code_to_id[lang_dict[output_lang]]
            )
            translated_queries = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

            for j in range(start, min(start+batch_size,len(data))):
                query_id = data[j]["query_id"] + output_lang
                queries_file.write(json.dumps({"query_id": query_id, "query": translated_queries[i]}) + "\n")

                new_row = {"context_id":data[j]["context_id"], "query_id": query_id, "orig_query_id": data[j]["query_id"], "context_lang":input_lang, "query_lang":output_lang}
                output_file.write(json.dumps(new_row) + "\n")

            print("Finished translating {n} rows from {input_lang} to {output_lang}".format(n=min(start+batch_size,len(data)), input_lang=input_lang,output_lang=output_lang))

    #Close the files
    output_file.close()
    queries_file.close()

    print("Saved to {output_filename}\n".format(output_filename=output_filename))
