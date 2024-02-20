#!/bin/bash 

# STEM_PATH=/home/katelyn/Documents/COSC490/Stemming
# MAIN_DIR=/home/katelyn/Desktop/PreTREC
# ATIRE_PATH=/home/katelyn/Documents/COSC490/SearchEngines/ATIRE

STEM_PATH=/home/katelyn/Documents/COSC490/Stemming
MAIN_DIR=/home/katelyn/Documents/preTREC
ATIRE_PATH=/home/katelyn/Documents/COSC490/ATIRE

COLLECTION=$1
COL=$2

: > $STEM_PATH/preTrec/BM25/$COL\_params

cd $ATIRE_PATH

declare -a k1_values=()
declare -a b_values=()

for stemmer in h k s Xe Xl w -
do

declare -a results=()
declare -a MAP_results=()

    for k1 in $(seq 2.7 0.1 5)
    do 
        for b in $(seq 0 0.1 1)
        do
            MAP=$(./bin/atire -t$stemmer -findex $MAIN_DIR/$COLLECTION/$COL.aspt -q$MAIN_DIR/$COLLECTION/$COL\-1.queries -a/$MAIN_DIR/$COLLECTION/$COL.qrels -RBM25:$k1:$b | tail -n 5 | head -n 1 | cut -d " " -f 2)
            results+=($k1 $b $MAP)
            MAP_results+=($MAP)
        done 
    done

    best_MAP=($(printf '%s\n' "${MAP_results[@]}" | sort -nr | cut -d " " -f 1))

    for i in "${!results[@]}"; do
        if [[ ${results[$i]} == "$best_MAP" ]]; then
            best_params=($(echo "${results[@]:$i-2:2}"))
        fi
    done

    echo "stemmer:-t$stemmer, k1:${best_params[0]}, b:${best_params[1]}, MAP:$best_MAP" >> $STEM_PATH/preTrec/BM25/$COL\_params
    k1_values+=("${best_params[0]}")
    b_values+=("${best_params[1]}")

done

echo "${k1_values[@]}" >> $STEM_PATH/preTrec/BM25/$COL\_params
echo "${b_values[@]}" >> $STEM_PATH/preTrec/BM25/$COL\_params