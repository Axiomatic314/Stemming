#! /bin/bash

STEMMING_PATH='/home/katelyn/Documents/COSC490/Stemming'

python cluster.py $STEMMING_PATH/Stemmers/krovetz/wikt krovetz y
python cluster.py $STEMMING_PATH/Stemmers/lovins/wikt lovins y
python cluster.py $STEMMING_PATH/Stemmers/sStripping/wikt sStripping y
python cluster.py $STEMMING_PATH/Stemmers/paiceHusk/wikt paiceHusk y
python cluster.py $STEMMING_PATH/Stemmers/porter2/wikt porter2 y
