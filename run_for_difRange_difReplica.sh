#!/bin/bash
echo "Removing old files................";
rm -rf terrace_output
rm -rf out
echo "Running Preprocessing......................";
./run_preProcessor.sh

echo "Finding Terraces for different ranges......";
MISSING_RANGE_LIST="$1"
ReplicaList="$2"
Field_Separator=$IFS
echo $MISSING_RANGE_LIST
echo $ReplicaList
# set comma as internal field separator for the string list
IFS=", "
mkdir -p terrace_output
for val in $MISSING_RANGE_LIST;
do
 x=$val
 for replica in $ReplicaList;
 do
    filename=$x"_"$replica"_gt_species.txt"
    ./run_RAxML_NG_forReplicas.sh $x $replica> terrace_output/$filename
 done
done

IFS=$Field_Separator

echo "Calculating RF Score............";
python checkRF_Score.py
# echo "Calculating Quartet Score........";
# python checkQuartetScore.py
echo "Done..............................";
