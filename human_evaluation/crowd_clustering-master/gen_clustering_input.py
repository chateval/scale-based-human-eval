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
    filepaths = [directory + "/" + file for file in files]

    for path in filepaths:
        with open(path, 'rb') as f:
            outputs = json.load(path)

            for k,v in outputs.items():
                print(k)
                print(v)
                new_sys = a

def main(system_outputs_folder):
    examples = load_directory(system_outputs_folder)
    
    

if __name__ == '__main__':
    system_outputs_folder = sys.argv[1]
    main(system_outputs_folder)
