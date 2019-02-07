import sys
import os
from os import listdir
from os.path import isfile, join
import json
import random

## Gets name of files in a list from a directory
def get_all_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    return files

## Load all json files!
def load_directory(directory):
    files = get_all_files(directory)[:1]
    filepaths = [directory + "/" + file for file in files]

    inputs, preds, scores = [], [], []
    for path in filepaths:
        inps, prds, scrs = [], [], []
        with open(path) as f:
            outputs = json.load(f)

            for result_dict in outputs["results"]:
                inps.append(' '.join(result_dict["input"]))
                prds.append([" ".join(p) for p in result_dict["pred"]])
                scrs.append(result_dict["scores"])
        inputs.append(inps)
        preds.append(prds)
        scores.append(scrs)

    print(len(inputs))
    print(inputs[0][0])
    print(preds[0][0])
    print(scores[0][0])

    return inputs, preds, scores

def output_format(inputs, preds, scores, output_base):
    
                

def main(system_outputs_folder):
    random.seed(37)
    inputs, preds, scores = load_directory(system_outputs_folder)
    
    

if __name__ == '__main__':
    system_outputs_folder = sys.argv[1]
    main(system_outputs_folder)

'''
python3 gen_clustering_input.py \
/data2/the_beamers/the_beamers_reno/experiments/10decodes/
'''
