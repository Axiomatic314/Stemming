#!/bin/bash

COLLECTION=$1

if [[ -z $COLLECTION ]]; then
	echo "invalid collection"
	exit
elif [ $COLLECTION == "collectionSize" ]; then
	COL="cs"
	SUBSETARR=("256" "128" "64" "32" "16" "8" "4" "2")
elif [ $COLLECTION == "documentLength" ]; then
	COL="dl"
	SUBSETARR=("20" "55" "148" "403" "1097" "2981" "all")
elif [ $COLLECTION == "combined" ]; then
	COL="dl_cs"
	SUBSETARR=("20-64" "55-32" "148-16" "403-8" "1097-4" "2981-2")
else
	echo "invalid collection"
	exit
fi

for subset in "${SUBSETARR[@]}"
do
	#./clueweb_output.sh $COLLECTION $COL $subset
	echo "$COLLECTION $COL $subset"
done
