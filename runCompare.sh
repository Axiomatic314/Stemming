#! /bin/bash

STEMMING_PATH='/home/katelyn/Documents/COSC490/Stemming'

python compare.py $STEMMING_PATH/Stemmers/krovetz/wikt krovetz
python compare.py $STEMMING_PATH/Stemmers/lovins/wikt lovins
python compare.py $STEMMING_PATH/Stemmers/sStripping/wikt sStripping
python compare.py $STEMMING_PATH/Stemmers/paiceHusk/wikt paiceHusk
python compare.py $STEMMING_PATH/Stemmers/porter2/wikt porter2
