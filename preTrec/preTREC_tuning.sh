#!/bin/bash 

# STEM_PATH=/home/katelyn/Documents/COSC490/Stemming
# PRETREC_PATH=/home/katelyn/Desktop/PreTREC
# ATIRE_PATH=/home/katelyn/Documents/COSC490/SearchEngines/ATIRE

STEM_PATH=/home/katelyn/Documents/COSC490/Stemming
PRETREC_PATH=/home/katelyn/Documents/preTREC
ATIRE_PATH=/home/katelyn/Documents/COSC490/ATIRE
TREC_EVAL_PATH="/home/katelyn/Documents/COSC490/trec_eval"

stem=(h k s Xe Xl w -)
stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")

COLLECTION=$1
COL=$2
LOW=$3
HIGH=$4

$STEM_PATH/preTrec/grid_search.sh $COLLECTION $COL $(($LOW-1)) >  $STEM_PATH/preTrec/BM25/$COL\_params
k1_values=$(cat $STEM_PATH/preTrec/BM25/$COL\_params | tail -n 2 | head -n 1)
b_values=$(cat $STEM_PATH/preTrec/BM25/$COL\_params | tail -n 1)
k1=($k1_values)
b=($b_values)

cd $ATIRE_PATH

for i in "${!stemmer[@]}"
do
    ./bin/atire -t"${stem[$i]}" -RBM25:"${k1[$i]}":"${b[$i]}" -findex $PRETREC_PATH/$COLLECTION/$COL.aspt -q$PRETREC_PATH/$COLLECTION/$COL\-$LOW\-$HIGH.queries -et -o$PRETREC_PATH/$COLLECTION/$COL\-"${stemmer[$i]}".out
done

cd $TREC_EVAL_PATH

echo "stemmer qid map" > $STEM_PATH/Data/pre\-trec/$COL\-MAP
for s in "${stemmer[@]}"
do
    : > $STEM_PATH/preTrec/$COL-temp
    ./trec_eval $PRETREC_PATH/$COLLECTION/$COL.qrels $PRETREC_PATH/$COLLECTION/$COL\-$s.out -q -m map | cut -f 2,3 >> $STEM_PATH/preTrec/$COL-temp
    while read -r line
    do
        echo "${s} $line"
    done < $STEM_PATH/preTrec/$COL-temp >> $STEM_PATH/Data/pre\-trec/$COL\-MAP
done

rm $STEM_PATH/preTrec/$COL-temp
