#!/bin/bash
# All decoding experiments for the paper should go here.

set -e 
set -o pipefail
   
NUM_DECODES=$1
BATCH_SIZE="10"
ROOT_DIR=".."
TRANSLATE="${ROOT_DIR}/OpenNMT-daphne/translate.py" 
SOURCE_FILE="eval_data/CMDB_prompt_subset.txt"
OUTPUT_DIR="experiments/${NUM_DECODES}decodes"
# MODEL="${ROOT_DIR}/models/opensubtitles_2_6_t_given_s_acc_31.62_ppl_43.79_e10.pt" 
MODEL="${ROOT_DIR}/models/opensubtitles_2_6_t_given_s_acc_32.66_ppl_38.81_e10.pt"
SEED="666"
GPU=2

mkdir -p $OUTPUT_DIR

echo "Diverse beam search"
python3 "$TRANSLATE" \
-model "$MODEL" \
-src "$SOURCE_FILE" \
-output "${OUTPUT_DIR}/diverse_beam_search_bs"${NUM_DECODES}"_dbs0.8.json" \
-beam_size "${NUM_DECODES}" \
-n_best "${NUM_DECODES}" \
-max_length 50 \
-block_ngram_repeat 0 \
-replace_unk \
-batch_size 1 \
-hamming_penalty 0.8 \
-gpu "${GPU}"
