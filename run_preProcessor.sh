#mkdir -p in
# cp dataset/taxa-37/gene-tree/noscale.200g.500b/1_gt.tre in/
#cp dataset/15-taxon/100gene-100bp/1_gt.tre in/
python3 preprocessor.py
python3 postprocessor.py