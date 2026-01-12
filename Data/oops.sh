#!/bin/bash

nARR=(2 4 8 16 32 64)
sizeARR=(25818901 12909723 6454615 3227227 1613766 806826)
lengthARR=(2981 1097 403 148 55 20)

cd combined

for i in "${!nARR[@]}"
do
    n="${nARR[$i]}"
    size="${sizeARR[$i]}"
    length="${lengthARR[$i]}"
    : > temp
    cat ndcg_$length-$n | while read line; do echo "${line} ${n} ${size} ${length}" >> temp; done
    sed '1c stemmer qid ndcg n collectionSize maxLength' -i temp
    mv temp ndcg_$length-$n
done
