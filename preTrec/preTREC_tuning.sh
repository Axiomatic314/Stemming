#!/bin/bash 

STEM_PATH=/home/harka424/Documents/COSC490/Stemming
PRETREC_PATH=/home/harka424/Documents/COSC490/preTREC
ATIRE_PATH=/home/harka424/Documents/COSC490/ATIRE
TREC_EVAL_PATH="/home/harka424/Documents/trec_eval"

stem=(h k s Xe Xl w -)
stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")
subsets=("cisi" "cran" "cf" "npl" "time")
collections=("CISI" "Cranfield" "CysticFibrosis" "NPL" "Time")

for subset in "${!subsets[@]}"
do

$STEM_PATH/preTrec/grid_search.sh "${collections[$subset]}" "${subsets[$subset]}" >  $STEM_PATH/preTrec/BM25/"${subsets[$subset]}"\_params
k1_values=$(cat $STEM_PATH/preTrec/BM25/"${subsets[$subset]}"\_params | tail -n 2 | head -n 1)
b_values=$(cat $STEM_PATH/preTrec/BM25/"${subsets[$subset]}"\_params | tail -n 1)
k1=($k1_values)
b=($b_values)

cd $ATIRE_PATH

for i in "${!stemmer[@]}"
do
    ./bin/atire -t"${stem[$i]}" -RBM25:"${k1[$i]}":"${b[$i]}" -findex $PRETREC_PATH/"${collections[$subset]}"/"${subsets[$subset]}".aspt -q$PRETREC_PATH/"${collections[$subset]}"/"${subsets[$subset]}"\-2.queries -et -o$PRETREC_PATH/"${collections[$subset]}"/"${subsets[$subset]}"\-"${stemmer[$i]}".out
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