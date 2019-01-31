#!/bin/sh
# All decoding experiments for the paper should go here.

set -e 
set -o pipefail
   
ROOT_DIR=".."
TRANSLATE="${ROOT_DIR}/OpenNMT-daphne/translate.py" 
SOURCE_FILE="${ROOT_DIR}/data/dbdc_eval_minus_CIC_200rand.txt"
OUTPUT_DIR="${ROOT_DIR}/decoding_experiments"
MODEL="${ROOT_DIR}/models/opennmt_sample_model.pt" 
SEED="666"

mkdir -p $OUTPUT_DIR

# Standard beam search, beam size 10
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/standard_beam_search_bs10.json" \
-beam_size 10 \
-max_length 50 \
-block_ngram_repeat 0 \
-replace_unk \
-batch_size 10 \
-seed "$SEED" \
-fast \
-n_best 10 \
-gpu 2

# Standard beam search, beam size 10, npad 0.3
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/standard_beam_search_bs10_npad0.3.json" \
-beam_size 10 \
-max_length 50 \
-block_ngram_repeat 0 \
-replace_unk \
-batch_size 10 \
-seed "$SEED" \
-fast \
-n_best 10 \
-hidden_state_noise 0.3 \
-gpu 2

# Random sampling, temperature=1.0
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/random_sampling_temp1.0.json" \
-beam_size 1 \
-max_length 50 \
-block_ngram_repeat 0 \
-replace_unk \
-batch_size 10 \
-seed "$SEED" \
-fast \
-gpu 2 \
-num_random_samples 10 \
-random_sampling_temp 1.0 \
-random_sampling_topk -1 \

# Random sampling, temperature=0.7
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/random_sampling_temp0.7.json" \
-beam_size 1 \
-max_length 50 \
-block_ngram_repeat 0 \
-replace_unk \
-batch_size 10 \
-seed "$SEED" \
-gpu 2 \
-num_random_samples 10 \
-random_sampling_temp 0.7 \
-random_sampling_topk -1 \

# Random sampling, temperature=1.3
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/random_sampling_temp1.3.json" \
-beam_size 1 \
-max_length 50 \
-block_ngram_repeat 0 \
-replace_unk \
-batch_size 10 \
-seed "$SEED" \
-gpu 2 \
-num_random_samples 10 \
-random_sampling_temp 1.3 \
-random_sampling_topk -1

# Random sampling, temperature=1.0, sample from top 10.
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/random_sampling_temp1.0_top10.json" \
-beam_size 1 \
-max_length 50 \
-block_ngram_repeat 0 \
-replace_unk \
-batch_size 10 \
-seed "$SEED" \
-gpu 2 \
-num_random_samples 10 \
-random_sampling_temp 1.0 \
-random_sampling_topk 10

## K Per Candidate beam search!
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/standard_beam_search_bs10_kpercand3.json" \
-beam_size 10 \
-n_best 10 \
-max_length 50 \
-block_ngram_repeat 1 \
-replace_unk \
-gpu 1 \
-batch_size 1 \
-k_per_cand 3


## Diverse beam search!
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/standard_beam_search_bs10_dbs0.8.json" \
-beam_size 10 \
-n_best 10 \
-max_length 50 \
-block_ngram_repeat 1 \
-replace_unk \
-gpu 0 \
-batch_size 1 \
-hamming_penalty 0.8


## Iterative beam search!
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/standard_beam_search_bs5_ibs10.json"
-beam_size 5 \
-n_best 5 \
-max_length 50 \
-block_ngram_repeat 1 \
-replace_unk \
-gpu 1 \
-batch_size 1 \
-beam_iters 10


## Clustering beam search!
## (NOTE: This takes longer because it loads in GloVe embeddings)
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/standard_beam_search_bs10_cbs5.json"
-beam_size 10 \
-n_best 10 \
-max_length 50 \
-block_ngram_repeat 1 \
-replace_unk \
-gpu 0 \
-batch_size 1 \
-num_clusters 5 \
-cluster_embeddings_file /data1/embeddings/eng/glove.42B.300d.txt
