import os
from .utils.file import join_dir

# taxa removal from each gene tree
# REMOVED_TAXA_RANGE = ['1-2', '3-4', '5-6', '7-8', '9-10', '11-12', '13-14', '15-16', '17-18', '19-20', '21-22', '23-24', '25-26', '27-28', '29-30']
REMOVED_TAXA_RANGE = []
RANGE_SEPARATOR = '-'

# === constants
NUMBER_OF_REPLICA = 20
REPLICA_LIST = [12]
NUM_TREES = 200
NUM_TAXA = 37
NUM_ORIENTATION = 3


# input output folders
INPUT_FOLDER = 'in'
OUTPUT_FOLDER = 'out'
WORKING_FOLDER = 'tmp'
TRUE_FOLDER = 'true'
CODES_FOLDER = 'codes'
TERRACE_OUTPUT_FOLDER = 'terrace_output'
SCRIPT_FOLDER = join_dir(CODES_FOLDER, 'scripts')
STATS_FOLDER = join_dir(OUTPUT_FOLDER, 'stats')
SCRIPT_FOLDER_DEPTH = 2

INPUT_FOLDER = join_dir(os.getcwd(), INPUT_FOLDER)
OUTPUT_FOLDER = join_dir(os.getcwd(), OUTPUT_FOLDER)
WORKING_FOLDER = join_dir(os.getcwd(), WORKING_FOLDER)
SCRIPT_FOLDER = join_dir(os.getcwd(), SCRIPT_FOLDER)
CODES_FOLDER = join_dir(os.getcwd(), CODES_FOLDER)

COMPLETE = 'complete'
INCOMPLETE = 'incomplete'

# IMPUTED = 'imputed'
PREDICTED = 'predicted'
PREDICTED_WITH_THRESHOLD = 'predicted_with_threshold'
PREDICTED_WITH_DISTRIBUTION = 'predicted_with_distribution'

# IMPUTED_LIST = [IMPUTED, PREDICTED,  PREDICTED_WITH_THRESHOLD, PREDICTED_WITH_DISTRIBUTION]
# IMPUTED_LIST = [IMPUTED, PREDICTED]
IMPUTED_LIST = []

MODES_LIST = [COMPLETE, INCOMPLETE]
# MODES_LIST = [INCOMPLETE]


# tree extension
GENE_TREE_SET_EXTENSION = '.tre'
NUMPY_EXTENSION = '.npy'
QUARTETS_EXTENSION = '.qrts'

GENE_TREE = 'gt'

ASTRAL = 'astral'
WQFM = 'wQFM'
TRUE_ST = 'true_st'



# METHODS = [WQFM]
METHODS = [ASTRAL]

FOUR_TAXA_MAP = 'map'

NUMPY_ARRAY = 'numpy'
QUARTETS = 'quartets'

SM_ASTRAL = 1
SM_wQFM = 2
SM_wQFC = 3

THRESHOLD_OF_REFUSE_PREDICTION = 0.70


MISSING_BY_CLADE = True
OUTGROUP_NAME = 'GAL'
MAX_TIMES_DELETION_HAPPEN = 3


ASTEROID_RAxML_NG = 'asteroid_raxml_ng'
ASTRID_RAxML_NG = 'astrid_raxml_ng'
ASTRALMP_RAxML_NG = 'astralmp_raxml_ng'
ASTRID_FASTME_RAxML_NG = 'astrid_fastme_raxml_ng'
BIPSTEP_RAxML_NG = 'bipstep_raxml_ng'
FASTRFS_RAxML_NG_GREEDY = 'fastrfs_raxml_ng_greedy'
FASTRFS_RAxML_NG_SINGLE = 'fastrfs_raxml_ng_SINGLE'
FASTRFS_RAxML_NG_SINGLE_life92 = 'fastrfs_SINGLE_life92'
FASTRFS_GREEDY_life92 = 'fastrfs_greedy_life92'
ASTRID_life92 = 'astrid_life92'
ASTEROID_life92 = 'asteroid_life92'
ASTRID_FASTME_life92 = 'astrid_fastme_life92'
ASTRAL_TRUE_life92 = 'astral_true_life92'
ASTRALMP_life92 = 'astralmp_life92'
# dictionary of mapping from method name to method species tree
METHOD_TO_ST = {
    ASTEROID_RAxML_NG: "asteroid-raxml-ng.GTR+G.speciesTree.newick",
    ASTRID_RAxML_NG: "asteroidastrid-raxml-ng.GTR+G.speciesTree.newick",
    ASTRALMP_RAxML_NG: "astralmp_raxml-ng.GTR+G.speciesTree.newick",
    ASTRID_FASTME_RAxML_NG: "astrid-fastme_raxml-ng.GTR+G.speciesTree.newick",
    BIPSTEP_RAxML_NG: "bipstep_raxml-ng.GTR+G.speciesTree.newick",
    FASTRFS_RAxML_NG_GREEDY: "fastrfs-raxml-ng_greedy.GTR+G.speciesTree.newick",
    FASTRFS_RAxML_NG_SINGLE: "fastrfs-raxml-ng_single.GTR+G.speciesTree.newick",
    FASTRFS_RAxML_NG_SINGLE_life92: "fastrfs-true_single.true.speciesTree.newick",
    FASTRFS_GREEDY_life92 : "fastrfs-true_greedy.true.speciesTree.newick",
    ASTRID_life92 : "astrid-fastme_true.true.speciesTree.newick",
    ASTEROID_life92 : "asteroid-true.true.speciesTree.newick",
    ASTRID_FASTME_life92 : "astrid-fastme_true.true.speciesTree.newick",
    ASTRAL_TRUE_life92 : "astral_true.true.speciesTree.newick",
    ASTRALMP_life92:'astralmp_true-additional.true.speciesTree.newick',

}

