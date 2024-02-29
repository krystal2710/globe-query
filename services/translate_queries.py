import json
from dotenv import load_dotenv
load_dotenv()

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
    
def translate_all(input_filename, input_lang, output_filename, output_lang_lists):
    """
    Translates the queries in the input file from the input language to multiple output languages and saves to an output file.
    """
    print("Translating {input_filename}".format(input_filename=input_filename))

    with open(input_filename) as input_file:
        data = json.load(input_file)
    
    output_file = open(output_filename, 'w')
    
    for output_lang in output_lang_lists:
        for i, row in enumerate(data):
            try:
                translated_query = translate_text(output_lang, row["question"])
                new_row = {"context":row["context"], "question": translated_query, "qid": row["qid"], "context_lang":input_lang, "query_lang":output_lang}
                output_file.write(json.dumps(new_row) + "\n")
            except:
                print("Error translating row {i} with qid {qid}".format(i=i, qid=row["qid"]))

            if i % 100 == 0:
                print("Translated {i} rows".format(i=i))

        print("Done translating from {input_lang} to {output_lang}".format(input_lang=input_lang, output_lang=output_lang))

    output_file.close()
    print("Saved to {output_filename}\n".format(output_filename=output_filename))
