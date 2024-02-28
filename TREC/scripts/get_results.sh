#!/bin/bash

ATIRE_PATH="/home/katelyn/Documents/COSC490/ATIRE"
TREC_PATH="/home/katelyn/Documents/TREC"
EVAL_PATH="/home/katelyn/Documents/COSC490/trec_eval"

SUB=$1
LOW=$2
HIGH=$3

stem=(h k s Xe Xl w -)
stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")

k1_values=$(cat $TREC_PATH/BM25/TREC\-$SUB-1 | tail -n 2 | head -n 1)
b_values=$(cat $TREC_PATH/BM25/TREC\-$SUB-1 | tail -n 1)
k1=($k1_values)
b=($b_values)

cd $ATIRE_PATH

for i in "${!stemmer[@]}"
do
	./bin/atire -t"${stem[$i]}" -RBM25:"${k1[$i]}":"${b[$i]}" -findex $TREC_PATH/TREC\-$SUB/TREC\-$SUB.aspt -q$TREC_PATH/TREC\-$SUB/topics.$LOW\-$HIGH -a$TREC_PATH/TREC\-$SUB/$LOW\-$HIGH.qrels -et -o$TREC_PATH/output/TREC\-$SUB\-"${stemmer[$s]}".out
done

cd $EVAL_PATH

echo "stemmer qid map" > $TREC_PATH/map/tuned_map_TREC\-$SUB
for s in "${stemmer[@]}"
do
	: > $TREC_PATH/map/tuned_map_TREC\-$SUB\-temp
	./trec_eval $TREC_PATH/TREC-$SUB/$LOW\-$HIGH.qrels $TREC_PATH/output/TREC\-$SUB\-$s.out -q -m map | cut -f 2,3 >> $TREC_PATH/map/tuned_map_TREC\-$SUB
	while read -r line
	do
		echo "${s} $line"
		done < $TREC_PATH/map/tuned_map_TREC\-$SUB\-temp >> $TREC_PATH/map/tuned_map_TREC\-$SUB
done

rm $TREC_PATH/map/tuned_map_TREC\-$SUB\-temp


