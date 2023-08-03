#!/bin/bash

MISSING_RANGE_LIST="$1"
ReplicaNum="$2"
RE_RUN=0

find_terrace(){
    echo "Running Preprocessing......................";
    ./run_preProcessor.sh
    
    echo "Finding Terraces for different ranges......";
    Field_Separator=$IFS
    echo $MISSING_RANGE_LIST
    echo $ReplicaNum
    # set comma as internal field separator for the string list
    IFS=", "
    mkdir -p terrace_output
    for val in $MISSING_RANGE_LIST;
    do
        x=$val
        replica=$ReplicaNum
        filename=$x"_"$replica"_gt_species.txt"
        ./run_RAxML_NG_forReplicas.sh $x $replica> terrace_output/$filename
        file_path="terrace_output/"$filename
        line_count=$(wc -l < "$file_path" | awk '{print $1}')
        echo "Line count :" $line_count
        if [ $line_count -gt 3 ] 
        # && [ $line_count -lt 1500 ]
        then
            echo "Found terrace for range: " $x
        else
            echo "No terrace found for range: " $x
            RE_RUN=1
        fi
    done

    IFS=$Field_Separator
}
try=1
find_terrace
echo "Re-run value: " $RE_RUN
while [ $RE_RUN -eq 1 ] && [ $try -lt 20 ]
do
    RE_RUN=0
    try=$((try+1))
    echo "Re-running for different ranges............";
    find_terrace
done

echo "Tried " $try " times to find terraces for different ranges";

# echo "Calculating Quartet Score........";
# python checkQuartetScore.py
echo "Done..............................";
