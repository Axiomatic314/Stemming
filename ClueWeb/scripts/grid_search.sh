#!/bin/bash 

CLUEWEB_PATH=/home/harka424/ClueWeb
ATIRE_PATH=/projects/harka424/ATIRE
INDEX_PATH=/projects/harka424/ClueWeb

QRELS=qrels.ndeval.txt
QUERIES=web2013.topics.txt

COLLECTION=$1
COL=$2
SUBSET=$3

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
			ndcg=$(./bin/atire -t$stemmer -findex $INDEX_PATH/$COL/index\_$SUBSET.aspt -q$CLUEWEB_PATH/2013/$QUERIES -a$CLUEWEB_PATH/2013/$QRELS -RBM25:$k1:$b -mnDCGt:a -k10 -l10 | tail -n 5 | head -n 1 | cut -d " " -f 2)
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
	
	echo "stemmer:-t$stemmer, k1:${best_params[0]}, b:${best_params[1]}, nDCG:$best_ndcg"
	k1_values+=("${best_params[0]}")
	b_values+=("${best_params[1]}")
	
done

echo "${k1_values[@]}"
echo "${b_values[@]}"
