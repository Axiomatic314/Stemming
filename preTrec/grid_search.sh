#!/bin/bash

MAIN_DIR=/home/katelyn/Desktop/PreTREC
COLLECTION=CysticFibrosis
QRY=cf-1-50.queries
QRELS=cf.qrels
INDEX=cf.aspt

cd ~/Documents/COSC490/SearchEngines/ATIRE

declare -a results=()
declare -a MAP_results=()

for k1 in $(seq 0 0.1 3)
do 
    for b in $(seq 0 0.1 1)
    do
        MAP=$(./bin/atire -findex $MAIN_DIR/$COLLECTION/$INDEX -q$MAIN_DIR/$COLLECTION/$QRY -a/$MAIN_DIR/$COLLECTION/$QRELS -RBM25:$k1:$b | tail -n 5 | head -n 1 | cut -d " " -f 2)
        results+=($k1 $b $MAP)
        MAP_results+=($MAP)
    done 
done

best_MAP=($(printf '%s\n' "${MAP_results[@]}" | sort -nr | cut -d " " -f 1))

for i in "${!results[@]}"; do
    if [[ ${results[$i]} == "$best_MAP" ]]; then
        best_params=($(echo "${results[@]:$i-2:2}"))
    fi
done

echo "k1:${best_params[0]}, b:${best_params[1]}, MAP:$best_MAP"