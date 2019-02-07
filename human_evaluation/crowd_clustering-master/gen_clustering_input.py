import sys
import os
from os import listdir
from os.path import isfile, join
import json

## Gets name of files in a list from a directory
def get_all_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    return files

def load_directory(directory):
    files = get_all_files(directory)[:1]
    print(files)
    filepaths = [directory + "/" + file for file in files]

    inputs, preds, scores = [], [], []
    for path in filepaths:
        with open(path) as f:
            outputs = json.load(f)

            for result_dict in outputs["results"]:
                inputs.append(' '.join(result_dict["input"]))
                preds.append([" ".join(p) for p in result_dict["preds"]])
                scores.append(result_dict["scores"])

    print(len(inputs))
    print(inputs[0])
    print(preds[0])
    print(scores[0])

    return inputs, preds, scores

                
                

def main(system_outputs_folder):
    inputs, preds, scores = load_directory(system_outputs_folder)
    
    

if __name__ == '__main__':
    system_outputs_folder = sys.argv[1]
    main(system_outputs_folder)

'''
python3 gen_clustering_input.py \
/data2/the_beamers/the_beamers_reno/experiments/10decodes/
'''
