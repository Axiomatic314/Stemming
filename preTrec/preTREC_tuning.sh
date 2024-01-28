#!/bin/bash 

STEM_PATH=/home/katelyn/Documents/COSC490/Stemming
MAIN_DIR=/home/katelyn/Desktop/PreTREC
ATIRE_PATH=/home/katelyn/Documents/COSC490/SearchEngines/ATIRE

stem=(h k s Xe Xl w -)
stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")

COLLECTION=$1
COL=$2
LOW=$3
HIGH=$4

$STEM_PATH/preTrec/grid_search.sh >  $STEM_PATH/preTrec/BM25/$COL\_params
k1_values=$(cat $STEM_PATH/preTrec/BM25/$COL\_params | tail -n 2 | head -n 1)
b_values=$(cat $STEM_PATH/preTrec/BM25/$COL\_params | tail -n 1)
k1=($k1_values)
b=($b_values)

cd $ATIRE_PATH

echo "stemmer, defaultMAP, tunedMAP"

for i in "${!k1[@]}"
do
    defaultMAP=$(./bin/atire -t"${stem[$i]}" -findex $MAIN_DIR/$COLLECTION/$COL.aspt -q$MAIN_DIR/$COLLECTION/$COL\-$LOW\-$HIGH.queries -a/$MAIN_DIR/$COLLECTION/$COL.qrels | tail -n 5 | head -n 1 | cut -d " " -f 2)
    tunedMAP=$(./bin/atire -t"${stem[$i]}" -findex $MAIN_DIR/$COLLECTION/$COL.aspt -q$MAIN_DIR/$COLLECTION/$COL\-$LOW\-$HIGH.queries -a/$MAIN_DIR/$COLLECTION/$COL.qrels -RBM25:"${k1[$i]}":"${b[$i]}" | tail -n 5 | head -n 1 | cut -d " " -f 2)

    echo "${stemmer[$i]}, $defaultMAP, $tunedMAP"
done
