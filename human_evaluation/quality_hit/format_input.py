import sys
import os
from os import listdir
from os.path import isfile, join
import json
import random


## Gets name of files in a list from a directory
def get_all_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))
             and ".json" in f]
    return files

## Flattens a two-dimensional list   
def flatten(listoflists):
    list = [item for sublist in listoflists for item in sublist]
    return list

# Load all json files
def load_directory(dir1, dir2):
    files1 = get_all_files(dir1)
    paths1 = [dir1 + "/" + file for file in files1]

    files2 = get_all_files(dir2)
    paths2 = [dir2 + "/" + file for file in files2]

    files1 = ["original/" + f for f in files1]
    files2 = ["clustered/" + f for f in files2]

    filepaths = paths1 + paths2
    files = files1 + files2

    inputs, preds, scores, systems = [], [], [], []
    for i, path in enumerate(filepaths):
        inps, prds, scrs = [], [], []
        with open(path) as f:
            print(path)
            outputs = json.load(f)

            for result_dict in outputs["results"]:
                inps.append(' '.join(result_dict["input"]))
                prds.append([" ".join(p) for p in result_dict["pred"]])
                scrs.append(result_dict["scores"])

        for j in range(len(inps)):
            inps[j] = inps[j].replace('&apos;', "'")
            inps[j] = inps[j].replace('&#124;', "|")
            for k in range(len(prds[j])):
                prds[j][k] = prds[j][k].replace('&apos;', "'")
                prds[j][k] = prds[j][k].replace('&#124;', "'")
            
        inputs.append(inps)
        preds.append(prds)
        scores.append(scrs)
        systems.append([files[i] for j in range(len(inps))]) 

    print(len(inputs))
    print(inputs[0][0])
    print(preds[0][0])
    print(scores[0][0])
    print(systems[0][0])

    return flatten(inputs), flatten(preds), flatten(scores), flatten(systems)


    


def main(system_outputs_folder, clustered_outputs_folder, output_file):
    random.seed(37)

    inputs, preds, scores, systems = load_directory(system_outputs_folder, clustered_outputs_folder)
    
    
    

if __name__ == '__main__':
    system_outputs_folder = sys.argv[1]
    clustered_outputs_folder = sys.argv[2]
    output_file = sys.argv[3]
    main(system_outputs_folder, clustered_outputs_folder, output_file)


'''
python3 format_input.py \
/data2/the_beamers/the_beamers_reno/experiments/10decodes/ \
/data2/the_beamers/the_beamers_reno/experiments/100to10decodes/ \
input/input.csv

NOTE: NOT DONE!!!!
'''
