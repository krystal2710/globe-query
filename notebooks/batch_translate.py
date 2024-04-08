def main():
    #Import libraries for preprocessing step
    import os
    import sys
    import jsonlines
    import json

    from dotenv import load_dotenv
    load_dotenv()
    sys.path.append(os.getenv('ROOT_DIR'))

    #Create all constant variables
    PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
    TESTING_DATA_DIR = os.getenv('TESTING_DATA_DIR')

    DATA_LANG_DICT = {"squad":"en", "korquad":"ko", "fquad":"fr", "germanquad":"de", "uitviquad":"vi"}

    #translate data
    from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

    #Load translation model a.k.a mbart fine-tuned checkpt
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    model.cuda()
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    lang_dict = {"en":"en_XX", "de":"de_DE", "ko":"ko_KR", "vi":"vi_VN", "fr":"fr_XX"}

    #load original data
    with open(os.path.join(PROCESSED_DATA_DIR, "test.json")) as input_file:
        data = json.load(input_file)

    n = len(data)
    new_data = []
    query_dict = {}

    for row in data:
        new_data.append(row)
        if row["context_lang"] not in query_dict:
            query_dict[row["context_lang"]] = []
        query_dict[row["context_lang"]].append(row)
    print("Finished adding existing data to output file")

    batch_size = 8
    for output_lang in DATA_LANG_DICT.values():
        for input_lang in query_dict.keys():
            tokenizer.src_lang = input_lang

            if input_lang == output_lang:
                continue
            lang_data = query_dict[input_lang]
            num_batch = 0
            total_batch = int(len(lang_data)/batch_size)
            for start in range(0,len(lang_data),batch_size):
                batch = [lang_data[i]["query"] for i in range(start, min(start+batch_size,len(lang_data)))]
                
                encoded_inputs = tokenizer(batch, return_tensors="pt", padding=True).to("cuda")
                generated_tokens = model.generate(
                    **encoded_inputs,
                    forced_bos_token_id=tokenizer.lang_code_to_id[lang_dict[output_lang]]
                )
                translated_queries = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

                for i, j in enumerate(range(start, min(start+batch_size,len(lang_data)))):
                    new_row = {"query": translated_queries[i], "context":lang_data[i]["context"], "query_lang":output_lang, "context_lang":input_lang}
                    new_data.append(new_row)
                num_batch += 1
                print("Finished {num_batch}/{total_batch} translating from {input_lang} to {output_lang}\n".format(num_batch=num_batch, total_batch = total_batch, input_lang=input_lang, output_lang=output_lang))
            print("Finished translating from {input_lang} to {output_lang}".format(input_lang=input_lang, output_lang=output_lang))

    with open(os.path.join(TESTING_DATA_DIR, "test-batch-wrong.json"), "w") as file:
        json.dump(new_data, file)

if __name__ == "__main__":
    main()
