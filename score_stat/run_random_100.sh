#!/bin/usr/bash

run_sequence() {
    for i in $(seq 1 ${1}); do
    # generate sequence of avrg. length 319
    echo "generate sequence..."
    python random_acid_gen.py -l 319 -o short_sequence | water -brief -asequence short_sequence -bsequence batched_seq_db -outfile stdout -gapopen 11. -gapextend 1. | awk '/^# Score:/ {print $3;}' >> ${1}random
    done
}

# Do run for 100 
echo "generate sequences in 100 runs..."
run_sequence "100"

# Do some extra exploration
echo "generate sequences in 500 runs..."
run_sequence "500"

#echo "generate sequences in 1000 runs..."
#run_sequence "1000"

# redo the same thing with a totally normally distributed DB
echo "generate normally distributed sequences"
for i in {1..100}; do
    python random_acid_gen.py -l 319 -w True -o short_sequence_norm | water -brief -asequence short_sequence_norm -bsequence generated_norm_db -outfile stdout -gapopen 11. -gapextend 1. | awk '/^# Score:/ {print $3;}' >> norm_random
done
