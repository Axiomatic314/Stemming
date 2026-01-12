#!/bin/bash 

STEM_PATH=/home/harka424/Documents/COSC490/Stemming
PRETREC_PATH=/home/harka424/Documents/COSC490/preTREC
ATIRE_PATH=/home/harka424/Documents/COSC490/ATIRE
TREC_EVAL_PATH="/home/harka424/Documents/trec_eval"

stem=(h k s Xe Xl w -)
stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")
subsets=("adi" "cacm" "lisa" "med")
collections=("ADI" "CACM" "LISA" "Medline")

for subset in "${!subsets[@]}"
do

cd $ATIRE_PATH

# search with default BM25 values
for i in "${!stemmer[@]}"
do
    ./bin/atire -t"${stem[$i]}" -findex $PRETREC_PATH/"${collections[$subset]}"/"${subsets[$subset]}".aspt -q$PRETREC_PATH/"${collections[$subset]}"/"${subsets[$subset]}".queries -et -o$PRETREC_PATH/"${collections[$subset]}"/"${subsets[$subset]}"\-"${stemmer[$i]}".out
done

cd $TREC_EVAL_PATH

echo "stemmer qid map" > $STEM_PATH/Data/pre\-trec/"${subsets[$subset]}"\-MAP
for s in "${stemmer[@]}"
do
    : > $STEM_PATH/preTrec/"${subsets[$subset]}"-temp
    ./trec_eval $PRETREC_PATH/"${collections[$subset]}"/"${subsets[$subset]}".qrels $PRETREC_PATH/"${collections[$subset]}"/"${subsets[$subset]}"\-$s.out -q -m map | cut -f 2,3 >> $STEM_PATH/preTrec/"${subsets[$subset]}"-temp
    while read -r line
    do
        echo "${s} $line"
    done < $STEM_PATH/preTrec/"${subsets[$subset]}"-temp >> $STEM_PATH/Data/pre\-trec/"${subsets[$subset]}"\-MAP
done

rm $STEM_PATH/preTrec/"${subsets[$subset]}"-temp

done