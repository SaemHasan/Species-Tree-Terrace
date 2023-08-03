#./max-cut-tree qrtt='example_input_file_for_wQMC_20_leaves.txt' weights=on otre='output.dat'
#./max-cut-tree qrtt='Imputed_Quartets_16' weights=off otre='Species_tree_Imputed'
#./max-cut-tree qrtt='Output_Quartets_whole_gt_wqmc' weights=on otre='Species_tree_whole_genes_01'
#./max-cut-tree qrtt='Output_Quartets_incomplete_gt_wqmc' weights=on otre='Species_tree_incomplete_genes_01'
#./max-cut-tree qrtt='Output_Quartets_incomplete_gt_wqmc' weights=true otre='Species_tree_miss_tx_wqmc_01'
#./max-cut-tree qrtt='01_Missing_taxa_newick_wqmc.quartets' weights=on otre='Species_tree_incomplete_genes_01'

#./max-cut-tree qrtt='01_true-genes_newick_wqmc.quartets' weights=on otre='Species_tree_whole_genes_01'

./max-cut-tree qrtt='Gene_trees_15_nos_newick_wqmc.quartets' weights=on otre='Species_tree_15_gt_wqmc.tre'
