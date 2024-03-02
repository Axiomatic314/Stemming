#!/bin/bash

ATIRE_PATH=/home/katelyn/Documents/COSC490/ATIRE
GOV2_PATH=/home/katelyn/Documents/COSC490/GOV2
EVAL_PATH=/home/katelyn/Documents/COSC490/trec_eval

stem=(h k s Xe Xl w -)
stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")

cd $ATIRE_PATH

for i in "${!stemmer[@]}"
do
    ./bin/atire -t"${stem[$i]}" -findex $GOV2_PATH/index.aspt -q$GOV2_PATH/701-850.topics -a$GOV2_PATH/701-850.qrels -et -o$GOV2_PATH/output/"${stemmer[$i]}".out
done

cd $EVAL_PATH

echo "stemmer qid map" > $GOV2_PATH/map/map_gov2
for s in "${stemmer[@]}"
do
    : > $GOV2_PATH/map/temp
    ./trec_eval $GOV2_PATH/701-850.qrels $GOV2_PATH/output/$s.out -q -m map | cut -f 2,3 >> $GOV2_PATH/map/temp
    while read -r line
    do
        echo "${s} $line"
        done < $GOV2_PATH/map/temp >> $GOV2_PATH/map/map_gov2
done

rm $GOV2_PATH/map/temp