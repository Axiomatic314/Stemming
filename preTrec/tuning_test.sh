#!/bin/bash

MAIN_DIR=/home/katelyn/Desktop/PreTREC
COLLECTION=CysticFibrosis
QRY=cf-50-100.queries
QRELS=cf.qrels
INDEX=cf.aspt

k1=(3.0 2.8 3.0 2.8 3.0 2.8 3.0)
b=(1.0 0.9 0.9 0.9 0.9 1.0 0.8)
stem=(h k s Xe Xl w -)
stemmer=("paiceHusk" "krovetz" "sStripping" "porter2" "lovins" "wikt" "none")

cd ~/Documents/COSC490/SearchEngines/ATIRE

echo "stemmer, defaultMAP, tunedMAP"

for i in "${!k1[@]}"
do
    defaultMAP=$(./bin/atire -t"${stem[$i]}" -findex $MAIN_DIR/$COLLECTION/$INDEX -q$MAIN_DIR/$COLLECTION/$QRY -a/$MAIN_DIR/$COLLECTION/$QRELS | tail -n 5 | head -n 1 | cut -d " " -f 2)
    tunedMAP=$(./bin/atire -t"${stem[$i]}" -findex $MAIN_DIR/$COLLECTION/$INDEX -q$MAIN_DIR/$COLLECTION/$QRY -a/$MAIN_DIR/$COLLECTION/$QRELS -RBM25:"${k1[$i]}":"${b[$i]}" | tail -n 5 | head -n 1 | cut -d " " -f 2)

    echo "${stemmer[$i]}, $defaultMAP, $tunedMAP"
done
