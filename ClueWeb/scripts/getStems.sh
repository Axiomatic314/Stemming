#!/bin/bash

ATIRE_PATH='/home/harka424/Documents/COSC490/ATIRE'
STEMMING_PATH='/home/harka424/Documents/COSC490/Stemming'
WORDS_FILE='/home/harka424/Documents/COSC490/Stemming/Data/clueweb/stems/curatedClueWeb.words'

cd $ATIRE_PATH
echo "Processing Paice/Husk"
bin/index -th -rcsv $WORDS_FILE
bin/atire_doclist
mv doclist.aspt $STEMMING_PATH/Data/clueweb/stems/paiceHuskDoclist.aspt
bin/atire_dictionary -p -q -l > $STEMMING_PATH/Data/clueweb/stems/paiceHuskDictionary
cd $STEMMING_PATH
python ClueWeb/wordToStem.py paiceHusk

cd $ATIRE_PATH
echo "Processing Porter2"
bin/index -tXe -rcsv $WORDS_FILE
bin/atire_doclist
mv doclist.aspt $STEMMING_PATH/Data/clueweb/stems/porterDoclist.aspt
bin/atire_dictionary -p -q -l > $STEMMING_PATH/Data/clueweb/stems/porterDictionary
cd $STEMMING_PATH
python ClueWeb/wordToStem.py porter

cd $ATIRE_PATH
echo "Processing Wikt"
bin/index -tw -rcsv $WORDS_FILE
bin/atire_doclist
mv doclist.aspt $STEMMING_PATH/Data/clueweb/stems/wiktDoclist.aspt
bin/atire_dictionary -p -q -l > $STEMMING_PATH/Data/clueweb/stems/wiktDictionary
cd $STEMMING_PATH
python ClueWeb/wordToStem.py wikt

cd $ATIRE_PATH
echo "Processing None"
bin/index -t- -rcsv $WORDS_FILE
bin/atire_doclist
mv doclist.aspt $STEMMING_PATH/Data/clueweb/stems/noneDoclist.aspt
bin/atire_dictionary -p -q -l > $STEMMING_PATH/Data/clueweb/stems/noneDictionary
cd $STEMMING_PATH
python ClueWeb/wordToStem.py none