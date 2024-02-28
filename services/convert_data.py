import json

def convert_quad(input_filename, output_filename):
    with open(input_filename) as input_file:
        data = json.load(input_file)
        if "data" in data:
            data = data["data"]
        
    res = []
    for article in data:
        for p in article["paragraphs"]:
            for qas in p["qas"]:
                if not qas["answers"]:
                    continue
                curr_row = {"context": p["context"], "question": qas["question"], "qid": qas["id"], "answer": qas["answers"][0]["text"]}
                res.append(curr_row)
    
    with open(output_filename, 'w') as output_file:
        json.dump(res, output_file)
    
    print("Completed conversion of {input_filename}".format(input_filename=input_filename))
    print("Saved to {output_filename}".format(output_filename=output_filename))

def convert_cmrc(input_filename, output_filename):
    with open(input_filename) as input_file:
        data = json.load(input_file)
        if "data" in data:
            data = data["data"]

    res = []
    for p in data:
        for qas in p["qas"]:
            curr_row = {"context": p["context_text"], "question": qas["query_text"], "qid": qas["query_id"], "answer": qas["answers"][0]}
            res.append(curr_row)
    
    with open(output_filename, 'w') as output_file:
        json.dump(res, output_file)
    
    print("Completed conversion of {input_filename}".format(input_filename=input_filename))
    print("Save to {output_filename}".format(output_filename=output_filename))