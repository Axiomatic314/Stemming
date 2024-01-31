#!/bin/bash

CLUEWEB_PATH=/home/harka424/ClueWeb
ATIRE_PATH=/projects/harka424/ATIRE
INDEX_PATH=/projects/harka424/ClueWeb
EVAL_PATH=/projects/harka424/trec-web-2013/src/eval

QRELS=qrels.ndeval.txt
QUERIES=web2013.topics.txt

stem=(h k s Xe Xl w -)
stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")

COLLECTION=$1
COL=$2
SUBSET=$3

k1_values=$(cat $CLUEWEB_PATH/tuned/BM25/$COL\_$SUBSET | tail -n 2 | head -n 1)
b_values=$(cat $CLUEWEB_PATH/tuned/BM25/$COL\_$SUBSET | tail -n 1)
k1=($k1_values)
b=($b_values)

cd $ATIRE_PATH

for i in "${!stemmer[@]}"
do
	#./bin/atire -t"${stem[$i]}" -RBM25:"${k1[$i]}":"${b[$i]}" -findex $INDEX_PATH/$COL/index\_$SUBSET.aspt -q$CLUEWEB_PATH/2013/$QUERIES -a$CLUEWEB_PATH/2013/$QRELS -k10 -l10 -et -o$CLUEWEB_PATH/tuned/output/$COL\_$SUBSET\_"${stemmer[$i]}".out
	./bin/atire -t"${stem[$i]}" -RBM25:0.9:0.4 -findex $INDEX_PATH/$COL/index\_$SUBSET.aspt -q$CLUEWEB_PATH/2013/$QUERIES -a$CLUEWEB_PATH/2013/$QRELS -k10 -l10 -et -o$CLUEWEB_PATH/tuned/output/$COL\_$SUBSET\_"${stemmer[$i]}".out
done

cd $EVAL_PATH

echo "stemmer qid ndcg" > $CLUEWEB_PATH/tuned/ndcg/$COLLECTION/ndcg\_$SUBSET
for s in "${stemmer[@]}"
do
	: > $CLUEWEB_PATH/tuned/ndcg/$COLLECTION/$SUBSET-temp
	./ndeval $CLUEWEB_PATH/2013/$QRELS $CLUEWEB_PATH/tuned/output/$COL\_$SUBSET\_$s.out | tail -n +2 | cut -d "," -f 2,10 --output-delimiter=" " >> $CLUEWEB_PATH/tuned/ndcg/$COLLECTION/$SUBSET-temp
	while read -r line
	do
		echo "${s} $line"
	done < $CLUEWEB_PATH/tuned/ndcg/$COLLECTION/$SUBSET-temp >> $CLUEWEB_PATH/tuned/ndcg/$COLLECTION/ndcg\_$SUBSET
done

rm $CLUEWEB_PATH/tuned/ndcg/$COLLECTION/$SUBSET-temp


