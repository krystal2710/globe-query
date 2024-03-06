import jsonlines

def read_contexts(file_path):
    data = {}
    with jsonlines.open(file_path) as reader:
        for line in reader:
            data[line["context_id"]] = line["context"]
    return data

def read_queries(file_path):
    data = {}
    with jsonlines.open(file_path) as reader:
        for line in reader:
            data[line["query_id"]] = line["query"]
    return data