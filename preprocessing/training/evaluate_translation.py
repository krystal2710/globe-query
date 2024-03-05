import json
from evaluate import load

from dotenv import load_dotenv
load_dotenv()
import sys
import os
sys.path.append(os.getenv('ROOT_DIR'))

from services.translate_queries import translate_text
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

def read_data(filename):
    with open(filename, "r") as f:
        data = []
        for line in f:
            data.append(json.loads(line))
    return data

def translate_for_eval(data_filename):

    data = read_data(data_filename)
    
    #Load translation model a.k.a mbart fine-tuned checkpt
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    model.cuda()

    #Load bertscore architecture
    bertscore = load("bertscore")

    #initialize result dictionary
    res = {k1:{k2:0 for k2 in ["en", "de", "ko", "fr", "vi", "zh"]} for k1 in ["en", "de", "ko", "fr", "vi", "zh"]}

    #initialize input_lang dictionary
    lang_dict = {"en":"en_XX", "de":"de_DE", "ko":"ko_KR", "vi":"vi_VN", "zh":"zh_CN", "fr":"fr_XX"}

    for i, row in enumerate(data):

        #Translate the query using mbart
        tokenizer.src_lang = lang_dict[row["original_lang"]]
        encoded_inputs = tokenizer(row["original_query"], return_tensors="pt").to("cuda")
        generated_tokens = model.generate(
            **encoded_inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id[lang_dict[row["translated_lang"]]]
        )
        translated_query = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        
        #calculate bertscore
        score = float(bertscore.compute(predictions=translated_query, references=[row["translated_query"]], lang=row["translated_lang"])["f1"][0])
        res[row["original_lang"]][row["translated_lang"]] += score

        if i % 100 == 0:
            print("Evaluated {i} queries".format(i=i))
    
    for k1 in res:
        for k2 in res[k1]:
            if k1 == k2:
                res[k1][k2] = 1
                continue
            res[k1][k2] = round(res[k1][k2]/100,3)

    return res
    

def main():
    res = translate_for_eval("data/translation_evaluated/ggl_translate_sample.jsonl")

    with open("data/translation_evaluated/results.json", "w") as f:
        json.dump(res, f)

if __name__ == "__main__":
    main()

    


    
    

        