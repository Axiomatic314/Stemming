#! /bin/bash

ATIRE_BIN_PATH='/home/katelyn/Documents/COSC490/SearchEngines/ATIRE/bin'
STEMMING_PATH='/home/katelyn/Documents/COSC490/Stemming'

echo "Processing Paice/Husk"
cd $STEMMING_PATH/Stemmers/paiceHusk/wikt
$ATIRE_BIN_PATH/index -th -rcsv $STEMMING_PATH/Wiktionary/words.txt
$ATIRE_BIN_PATH/atire_doclist
$ATIRE_BIN_PATH/atire_dictionary -p -q -l > $STEMMING_PATH/Stemmers/paiceHusk/wikt/atire_dictionary
cd $STEMMING_PATH/Stemmers
python wordToStem.py paiceHusk/wikt paiceHusk/wikt/paiceHuskStems

echo "Processing Krovetz"
cd $STEMMING_PATH/Stemmers/krovetz/wikt
$ATIRE_BIN_PATH/index -tk -rcsv $STEMMING_PATH/Wiktionary/words.txt
$ATIRE_BIN_PATH/atire_doclist
$ATIRE_BIN_PATH/atire_dictionary -p -q -l > $STEMMING_PATH/Stemmers/krovetz/wikt/atire_dictionary
cd $STEMMING_PATH/Stemmers
python wordToStem.py krovetz/wikt krovetz/wikt/krovetzStems

echo "Processing S-Stripping"
cd $STEMMING_PATH/Stemmers/sStripping/wikt
$ATIRE_BIN_PATH/index -ts -rcsv $STEMMING_PATH/Wiktionary/words.txt
$ATIRE_BIN_PATH/atire_doclist
$ATIRE_BIN_PATH/atire_dictionary -p -q -l > $STEMMING_PATH/Stemmers/sStripping/wikt/atire_dictionary
cd $STEMMING_PATH/Stemmers
python wordToStem.py sStripping/wikt sStripping/wikt/sStrippingStems

echo "Processing Porter2"
cd $STEMMING_PATH/Stemmers/porter2/wikt
$ATIRE_BIN_PATH/index -tXe -rcsv $STEMMING_PATH/Wiktionary/words.txt
$ATIRE_BIN_PATH/atire_doclist
$ATIRE_BIN_PATH/atire_dictionary -p -q -l > $STEMMING_PATH/Stemmers/porter2/wikt/atire_dictionary
cd $STEMMING_PATH/Stemmers
python wordToStem.py porter2/wikt porter2/wikt/porter2Stems

echo "Processing Lovins"
cd $STEMMING_PATH/Stemmers/lovins/wikt
$ATIRE_BIN_PATH/index -tXl -rcsv $STEMMING_PATH/Wiktionary/words.txt
$ATIRE_BIN_PATH/atire_doclist
$ATIRE_BIN_PATH/atire_dictionary -p -q -l > $STEMMING_PATH/Stemmers/lovins/wikt/atire_dictionary
cd $STEMMING_PATH/Stemmers
python wordToStem.py lovins/wikt lovins/wikt/lovinsStems
