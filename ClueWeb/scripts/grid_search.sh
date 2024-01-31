#!/bin/bash 

CLUEWEB_PATH=/home/harka424/ClueWeb
ATIRE_PATH=/projects/harka424/ATIRE
INDEX_PATH=/projects/harka424/ClueWeb
EVAL_PATH=/projects/harka424/trec-web-2013/src/eval

QRELS=qrels.ndeval.txt
QUERIES=web2013.topics.txt

COLLECTION=$1
COL=$2
SUBSET=$3

: > $CLUEWEB_PATH/tuned/BM25/$COL\_$SUBSET

declare -a k1_values=()
declare -a b_values=()	

cd $ATIRE_PATH

for stemmer in h k s Xe Xl w -
do
	declare -a results=()
	declare -a ndcg_results=()
	
	for k1 in $(seq 0 0.1 3)
	do
		for b in $(seq 0 0.1 1)
		do
			./bin/atire -t$stemmer -findex $INDEX_PATH/$COL/index\_$SUBSET.aspt -q$CLUEWEB_PATH/2013/$QUERIES -a$CLUEWEB_PATH/2013/$QRELS -RBM25:$k1:$b -k10 -l10 -et -otemp.out
			ndcg=$($EVAL_PATH/ndeval $CLUEWEB_PATH/2013/$QRELS temp.out | tail -n 1 | cut -d ',' -f 10)
			
			results+=($k1 $b $ndcg)
			ndcg_results+=($ndcg)
		done
	done
	
	best_ndcg=($(printf '%s\n' "${ndcg_results[@]}" | sort -nr | cut -d " " -f 1))
	
	for i in "${!results[@]}"; do
		if [[ ${results[$i]} == "$best_ndcg" ]]; then
			best_params=($(echo "${results[@]:$i-2:2}"))
		fi
	done
	
	echo "stemmer:-t$stemmer, k1:${best_params[0]}, b:${best_params[1]}, nDCG:$best_ndcg" >> $CLUEWEB_PATH/tuned/BM25/$COL\_$SUBSET
	k1_values+=("${best_params[0]}")
	b_values+=("${best_params[1]}")
	
done

echo "${k1_values[@]}" >> $CLUEWEB_PATH/tuned/BM25/$COL\_$SUBSET
echo "${b_values[@]}" >> $CLUEWEB_PATH/tuned/BM25/$COL\_$SUBSET
