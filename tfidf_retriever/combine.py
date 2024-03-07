import argparse
import os
import json
import random


# Read the json dataset ====================================================
def read_dataset(path):
    f = open(path, "r")
    data = json.load(f)
    return data

def write_output(path_to_save, squad_form):
    if not os.path.exists(path_to_save):
        os.mknod(path_to_save)
        
    # Write the combined dataset to a JSON file
    with open(path_to_save, 'w') as f:
        json.dump(squad_form, f, indent=4)


# Combine unans candidate with answerable dataset ====================================================
def read(cdd_path, dataset_path):
    cdd_data = read_dataset(cdd_path)['data']
    ans_data = read_dataset(dataset_path)['data']

    return cdd_data, ans_data


def combine(cdd_path, dataset_path, save_path, num=False):
    cdd_data, ans_data = read(cdd_path, dataset_path)

    # select random number of unanswerable candidates
    cdd_select = random.sample(cdd_data, num if num != False else len(cdd_data))

    # Combine two data
    combine_data = cdd_select + ans_data

    # Write output
    combine_dataset = {'data': combine_data}
    write_output(save_path, combine_dataset)

    return combine_dataset


# Print out the number of ans and unans of the dataset ====================================================
def info(combine_dataset):
    ans, unans = 0, 0

    for item in combine_dataset['data']:
        if item['answers']['answer_start'] == []:
            unans += 1
        else:
            ans += 1

    print("Dataset info:")
    print("# of unans", unans)
    print("# of ans", ans)

