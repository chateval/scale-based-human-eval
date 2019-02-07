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

    for path in filepaths:
        with open(path) as f:
            outputs = json.load(f)

            for k,v in outputs.items():
                print(k)
                print(v)

                i = 0
                for item in v:
                    for k2, v2 in item.items():
                        if i == 0:                           
                            print(k2)
                            print(v2)
                        i += 1
        print("\n\n")

def main(system_outputs_folder):
    examples = load_directory(system_outputs_folder)
    
    

if __name__ == '__main__':
    system_outputs_folder = sys.argv[1]
    main(system_outputs_folder)

'''
python3 gen_clustering_input.py \
/data2/the_beamers/the_beamers_reno/experiments/10decodes/
'''
