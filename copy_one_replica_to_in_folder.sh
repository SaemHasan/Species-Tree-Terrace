x=$1
rm -r in
mkdir -p in
filename=$x
filename+="_gt.tre"
# echo $filename
cp dataset/taxa-37/gene-tree/noscale.200g.500b/$filename in/