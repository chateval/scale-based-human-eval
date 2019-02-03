import glob
import json
import csv
import editdistance
import nltk
from bert_serving.client import BertClient
from mosestokenizer import MosesDetokenizer

import configargparse
import numpy as np
import os


def eval_emb_stats(candidates):
  """Computed several statistics based on sequence embeddings.
  
  These include:
    * average distance of the embeddings from the mean embedding.
    * standard deviation of the 
  """

  bc = BertClient()
  detokenize = MosesDetokenizer('en')

  detoked_cands = []
  for cand in candidates:
    detoked_cands.append(detokenize(cand))
  detoked_cands = [c for c in detoked_cands if len(c) > 0]

  embs = bc.encode(detoked_cands)
  embs = [np.mean(emb, 0) for emb in embs]

  center = np.mean(embs, 0)
  # TODO(daphne): Would dot product be more correct?
  distances = [np.linalg.norm(center-emb) for emb in embs]
  return np.mean(distances)

def eval_distinct_k(candidates, k):
  """The total number of k-grams divided by the total number of tokens
     over all the candidates.
  """
  kgrams = set()
  total = 0
  for cand in candidates:
    if len(cand) < k:
      continue

    for i in range(0, len(cand)-k+1):
      kgrams.add(tuple(cand[i:i+k]))
    total += len(cand)
  if total == 0:
    print('Why does this happen sometimes?')
    import pdb; pdb.set_trace()
  return len(kgrams) / total

def eval_edit_distance(candidates):
  """The min, mean, and max pairwise edit-distance between candidates."""
  distances = []
  for idx in range(len(candidates)):
    for jdx in range(idx+1, len(candidates)):
      cand1 = candidates[idx]
      cand2 = candidates[jdx]
      dist = editdistance.eval(cand1, cand2)
      distances.append(dist)
  return min(distances), np.mean(distances), max(distances)


def main(opt):
  all_results = {}
  for json_file in glob.glob(os.path.join(opt.dir, '*.json')):
    with open(json_file, 'r') as f:
      try:
        experiment = json.load(f)
        print('Processing ' + json_file)
      except:
        print('Error processing ' + json_file)
        print('Skipping it.')

      exp_name = os.path.basename(json_file).replace('.json', '')

      eval_results = []

      for example in experiment['results']:
        candidates = example['pred']

        ex_results = {}
        ex_results['dist_from_mean_emb'] = eval_emb_stats(candidates)
        ex_results['num_distinct_1grams'] = eval_distinct_k(candidates, 1)
        ex_results['num_distinct_2grams'] = eval_distinct_k(candidates, 2)
        min_edit, mean_edit, max_edit = eval_edit_distance(candidates)
        ex_results['min_edit_distance'] = min_edit
        ex_results['mean_edit_distance'] = mean_edit
        ex_results['max_edit_distance'] = max_edit
        eval_results.append(ex_results)

    all_results[exp_name] = {'ex_results': eval_results,
                             'perplexity': experiment['ppl'],
                             'score': experiment['score']}

  keys = list(all_results[exp_name].keys())
  with open(os.path.join(opt.dir, 'results.csv'), 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['exp'] + keys)

    for json_file, results in all_results.items():
      means = []
      for key in keys:
        means.append(np.mean([r[key] for r in results]))
      writer.writerow([json_file] + means)


if __name__ == '__main__':
  parser = configargparse.ArgumentParser(
      description='analyze_diversity.py',
      config_file_parser_class=configargparse.YAMLConfigFileParser,
      formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
  group = parser.add_argument_group('Directory')
  group.add('--dir', type=str, help='Directory containing json files.')
  opt = parser.parse_args()

  main(opt)
