#!/bin/bash

ATIRE_PATH="/home/katelyn/Documents/COSC490/ATIRE"
TREC_PATH="/home/katelyn/Documents/TREC"
EVAL_PATH="/home/katelyn/Documents/COSC490/trec_eval"

SUBSET=$1
LOW=$2
HIGH=$3

: > $TREC_PATH/BM25/TREC\-$SUBSET

declare -a k1_values=()
declare -a b_values=()

cd $ATIRE_PATH

for stemmer in h k s Xe Xl w -
do
    declare -a results=()
    declare -a MAP_results=()

    for k1 in $(seq 0 0.1 3)
    do
        for b in $(seq 0 0.1 1)
        do
            ./bin/atire -t$stemmer -findex $TREC_PATH/TREC\-$SUBSET/TREC\-$SUBSET.aspt -q$TREC_PATH/TREC-$SUBSET/topics.$LOW\-$HIGH -a$TREC_PATH/TREC\-$SUBSET/$LOW-$HIGH.qrels -RBM25:$k1:$b -et -o$TREC_PATH/output/temp\-$SUBSET.out
            MAP=$($EVAL_PATH/trec_eval $TREC_PATH/TREC\-$SUBSET/$LOW\-$HIGH.qrels $TREC_PATH/output/temp\-$SUBSET.out -q -m -map | cut -f 2,3)

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
	
	echo "stemmer:-t$stemmer, k1:${best_params[0]}, b:${best_params[1]}, MAP:$best_MAP" >> $TREC_PATH/BM25/TREC\-$SUBSET
	k1_values+=("${best_params[0]}")
    b_values+=("${best_params[1]}")

done 

echo "${k1_values[@]}" >> $TREC_PATH/BM25/TREC\-$SUBSET
echo "${b_values[@]}" >> $TREC_PATH/BM25/TREC\-$SUBSET