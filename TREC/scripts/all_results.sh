#!/bin/bash

ATIRE_PATH="/home/harka424/Documents/COSC490/ATIRE"
TREC_PATH="/home/harka424/Documents/COSC490/TREC"
EVAL_PATH="/home/harka424/Documents/trec_eval"
STEM_PATH="/home/harka424/Documents/COSC490/Stemming/Data/trec"

query_low=1
for subset in $(seq 1 1 8)
do
    query_low=$((query_low + 50))
    query_high=$((query_low + 49))
    stem=(h k s Xe Xl w -)
    stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")

    cd $ATIRE_PATH

    #search with default bm25 values
    for i in "${!stemmer[@]}"
    do
        ./bin/atire -t"${stem[$i]}" -findex $TREC_PATH/TREC\-$subset/TREC\-$subset.aspt -q $TREC_PATH/TREC\-$subset/topics.$query_low\-$query_high -a$TREC_PATH/TREC\-$subset/$query_low\-$query_high.qrels -et -o$TREC_PATH/output/TREC\-$subset\-"${stemmer[$i]}".out
    done

    #evaluate results
    cd $EVAL_PATH
    
    echo "stemmer qid map" > $STEM_PATH/map_TREC\-$subset
    for s in "${stemmer[@]}"
    do
        : > $STEM_PATH/temp
        ./trec_eval $TREC_PATH/TREC\-$subset/$query_low\-$query_high.qrels $TREC_PATH/output/TREC\-$subset\-$s.out -q -m map | cut -f 2,3 >> $STEM_PATH/temp
        while read -r line
        do
            echo "${s} $line"
            done < $STEM_PATH/temp >> $STEM_PATH/map_TREC\-$subset
    done

    rm $STEM_PATH/temp


done