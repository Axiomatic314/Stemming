#!/bin/bash

ATIRE_BIN_PATH='/home/katelyn/Documents/COSC490/ATIRE/bin'
NDEVAL_PATH='/home/katelyn/Documents/COSC490/trec-web-2013'
CLUEWEB_PATH='/home/katelyn/Documents/COSC490/ClueWeb'
STEMMING_PATH='/home/katelyn/Documents/COSC490/Stemming/Data/clueweb-2013'
MEASURE='nDCG'
M=10

for N in 1 2 4 8 16 32 64 128 256
do
	cd $STEMMING_PATH/n-$N
    rm $MEASURE-$N
	: > $MEASURE-$N
	$NDEVAL_PATH/ndeval $CLUEWEB_PATH/2013/qrels.ndeval.txt paiceHusk-$N.out |tail -1 | cut -d ',' -f $M >> $MEASURE-$N
	$NDEVAL_PATH/ndeval $CLUEWEB_PATH/2013/qrels.ndeval.txt krovetz-$N.out |tail -1 | cut -d ',' -f $M >> $MEASURE-$N
	$NDEVAL_PATH/ndeval $CLUEWEB_PATH/2013/qrels.ndeval.txt sStripper-$N.out |tail -1 | cut -d ',' -f $M >> $MEASURE-$N
	$NDEVAL_PATH/ndeval $CLUEWEB_PATH/2013/qrels.ndeval.txt porter-$N.out |tail -1 | cut -d ',' -f $M >> $MEASURE-$N
	$NDEVAL_PATH/ndeval $CLUEWEB_PATH/2013/qrels.ndeval.txt lovins-$N.out |tail -1 | cut -d ',' -f $M >> $MEASURE-$N
	$NDEVAL_PATH/ndeval $CLUEWEB_PATH/2013/qrels.ndeval.txt wikt-$N.out |tail -1 | cut -d ',' -f $M >> $MEASURE-$N
	$NDEVAL_PATH/ndeval $CLUEWEB_PATH/2013/qrels.ndeval.txt none-$N.out |tail -1 | cut -d ',' -f $M >> $MEASURE-$N
done