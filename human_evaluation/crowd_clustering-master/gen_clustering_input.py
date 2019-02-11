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

## Flattens a two-dimensional list   
def flatten(listoflists):
    list = [item for sublist in listoflists for item in sublist]
    return list

## Load all json files!
def load_directory(directory):
    files = get_all_files(directory)
    filepaths = [directory + "/" + file for file in files]

    inputs, preds, scores, system_inds = [], [], [], []
    for i, path in enumerate(filepaths):
        inps, prds, scrs = [], [], []
        with open(path) as f:
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
        system_inds.append([i for j in range(len(inps))]) 

    print(len(inputs))
    print(inputs[0][0])
    print(preds[0][0])
    print(scores[0][0])
    print(system_inds[0][0])

    return flatten(inputs), flatten(preds), flatten(scores), flatten(system_inds)

## Return output format required
def output_format(inputs, preds, scores, system_inds, output_base):
    random_inds = [i for i in range(len(inputs))]
    random.shuffle(random_inds)

    with open(output_base + "_responses.txt", 'w', encoding='utf8') as f:
        for i in random_inds:
            f.write(inputs[i] + " === " + str(system_inds[i]) + " ::: ")

            prds = [preds[i][j] + " ||| " + str(scores[i][j]) for j in range(len(preds[i]))]
            f.write(" ;;; ".join(prds) + " ;;; \n")

    with open(output_base + "_prompts.txt", 'w', encoding='utf8') as f:
        for i in random_inds:
            f.write(inputs[i] + " === " + str(system_inds[i]) + "\n")
                

def main(system_outputs_folder, output_base):
    random.seed(37)
    inputs, preds, scores, system_inds = load_directory(system_outputs_folder)
    output_format(inputs, preds, scores, system_inds, output_base)

    
    
    

if __name__ == '__main__':
    system_outputs_folder = sys.argv[1]
    output_base = sys.argv[2]
    main(system_outputs_folder, output_base)

'''
python3 gen_clustering_input.py \
/data2/the_beamers/the_beamers_reno/experiments/10decodes/ \
hit_data/pp/input
'''
