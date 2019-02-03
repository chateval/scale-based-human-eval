import glob
import json
import csv
import editdistance
import nltk
from bert_serving.client import BertClient
from mosestokenizer import MosesDetokenizer
import collections

import configargparse
import numpy as np
import os


def get_embs(candidates):
  """Returns the sequence embedding for each candidate."""

  bc = BertClient()
  detokenize = MosesDetokenizer('en')

  detoked_cands = []
  for i, cand in enumerate(candidates):
    detoked_cands.append(detokenize(cand))
    if len(detokenize(cand)) == 0:
      print(i)
      print(cand)
      print(detokenize(cand))

  embs = bc.encode(detoked_cands)
  embs = [e / np.linalg.norm(e) for e in embs]
  # embs = [np.mean(emb, 0) for emb in embs]

  return embs

def remove_duplicates(candidates, scores):
  # counter = collections.Counter(' '.join(c) for c in candidates)
  new_candidates = []
  new_scores = []
  for cand, score in zip(candidates, scores):
    if cand not in new_candidates and len(cand) > 0:
      new_candidates.append(cand)
      new_scores.append(score)
  return new_candidates, new_scores

def main(opt):
  if not os.path.exists(opt.output_dir):
    os.makedirs(opt.output_dir)

  all_results = {}
  for json_file in glob.glob(os.path.join(opt.input_dir, '*.json')):
    with open(json_file, 'r') as f:
      try:
        experiment = json.load(f)
        print('Processing ' + json_file)
      except:
        print('Error processing ' + json_file)
        print('Skipping it.')
        continue

      for example in experiment['results']:
        candidates = example['pred']
        scores = example['scores']
        candidates, scores = remove_duplicates(candidates, scores)
        embs = get_embs(candidates)

        # Take the most likely candidate a sthe first to keep.
        most_likely_cand_idx = np.argmax(scores)
        cand_ids_to_keep = [most_likely_cand_idx]

        # At every step, choose the next candidate to be the one that is most
        # different from the ones that have been chosen so far.
        for _ in range(opt.num_cands - 1):
          best_idx_so_far = -1
          best_dist_so_far = 0.0
          for cdx, cand in enumerate(candidates):
            if cdx not in cand_ids_to_keep:
              d = sum(np.linalg.norm(embs[cdx] - embs[mdx]) for mdx in cand_ids_to_keep)
              if d > best_dist_so_far:
                best_dist_so_far = d
                best_idx_so_far = cdx
          cand_ids_to_keep.append(best_idx_so_far)
        example['pred'] = [candidates[cdx] for cdx in cand_ids_to_keep]
        example['scores'] = [scores[cdx] for cdx in cand_ids_to_keep]

    out_json_file = os.path.join(opt.output_dir, os.path.basename(json_file))
    with open(out_json_file, 'w') as f:
      json.dump(experiment, f)


if __name__ == '__main__':
  parser = configargparse.ArgumentParser(
      description='analyze_diversity.py',
      config_file_parser_class=configargparse.YAMLConfigFileParser,
      formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
  group = parser.add_argument_group('Arguments')
  group.add('--input_dir', type=str, required=True,
            help='Directory containing json files.')
  group.add('--output_dir', type=str, required=True,
            help='Directory to write out files.')
  group.add('--num_cands', type=int, default=10,
            help='The target number of candidates.')
  opt = parser.parse_args()

  main(opt)
