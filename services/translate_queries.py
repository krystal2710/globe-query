import json
from dotenv import load_dotenv
load_dotenv()

def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

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
    with open(input_filename) as input_file:
        data = json.load(input_file)
    
    res = []
    for row in data:
        for output_lang in output_lang_lists:
            new_row = {"context":row["context"], "question":translate_text(output_lang), "qid": row["qid"], "context_lang":input_lang, "query_lang":output_lang}
            res.append(new_row)
    
    with open(output_filename, 'w') as output_file:
        json.dump(res, output_file)
