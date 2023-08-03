x=$1
rm -r in
mkdir -p in
for ((i=1; i<$x+1; i++)) do
# echo $i
filename=$i
filename+="_gt.tre"
# echo $filename
cp dataset/taxa-37/gene-tree/noscale.200g.500b/$filename in/
done
