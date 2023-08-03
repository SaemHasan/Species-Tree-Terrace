#!/bin/bash
#FILES="/Species_trees/"
#cp AfterPhylo.pl Species_tree_Taxa_Removed/
#cd Species_tree_Taxa_Removed/
# $1 == input file 
# $2 == working directory
split_by () {
    string=$1
    separator=$2

    tmp=${string//"$separator"/$'\2'}
    IFS=$'\2' read -a arr <<< "$tmp"
    for substr in "${arr[@]}" ; do
        echo "$substr"
        # echo
    done
    # echo
}

file=$1
echo " processing $file"
# perl Codes/MISC/AfterPhylo.pl -unlabeled -topology $file
perl $2/AfterPhylo.pl -unlabeled -topology $file

file_parts=$(split_by $file '.tre')
output="$file_parts.out.tre"
echo $output
sed -i 's/; \?/;\n/g' "$output"
echo "Finally processed $output"
#rm $file		
#echo "$file_parts"
#perl AfterPhylo.pl -unlabeled -topology simtrees_1_spt.tre
#sed -i 's/; \?/;\n/g' simtrees_1_spt.out.tre
