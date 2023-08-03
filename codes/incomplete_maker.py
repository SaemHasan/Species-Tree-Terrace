import imp
import random
import time

import warnings

from codes.parameters import RANGE_SEPARATOR, MISSING_BY_CLADE, OUTGROUP_NAME

from codes.utils.gt import get_taxa_list_from_gt

import dendropy
from dendropy import Tree
from dendropy import TreeList

from codes.utils.file import create_file_abs

from codes.gt_handler import get_taxa_list_AND_gt_list

from ete3 import PhyloTree
import numpy as np


############################# dictionary of removed taxa #############################

taxon_left_count = {}

#######################################################################################


def get_deleted_taxa_without_removing_one(gt, count, preserved_taxon):
    taxa_list = get_taxa_list_from_gt(gt)
    assert len(taxa_list) >= count, "can't delete " + \
        count + " taxa from " + len(taxa_list)
    indexes = random.sample(range(0, len(taxa_list)), count)

    ret = []

    for i in indexes:
        if taxa_list[i] != preserved_taxon:
            ret.append(taxa_list[i])
    return ret


def save_taxa_from_extinction(taxa_list):
    global taxon_left_count
    ret = []
    for taxon in taxa_list:
        if taxon_left_count[taxon] > 1:
            taxon_left_count[taxon] -= 1
            ret.append(taxon)
        else:
            print("taxon ", taxon, " is saved from extinction ")
            pass
    print('ret from extinction : ', ret, 'taxa_list : ', taxa_list)
    return ret


def get_deleted_taxa(gt, count):
    taxa_list = get_taxa_list_from_gt(gt)
    assert len(taxa_list) >= count, "can't delete " + \
        count + " taxa from " + len(taxa_list)
    indexes = random.sample(range(0, len(taxa_list)), count)
    # warnings.warn("how on earth this is conserving one taxa ??? --> need discussion ")

    return save_taxa_from_extinction([taxa_list[i] for i in indexes])


def get_deleted_taxa_by_clade(gt, count):
    print('we are here')
    tree = PhyloTree(gt + ';')

    # times we will go for deletion a small portion of taxa

    times_broken = 0
    #selecting the outgroup randomly
    # outgroup = random.choice(tree.get_leaves()).name
    # tree.set_outgroup(outgroup)
    root_node = tree.get_tree_root()
    print(count)
    # print(root_node.get_ascii(show_internal=True))
    ret_taxa = []
    iter = True
    while root_node.is_leaf() == False and count > 0:
        try:
            left_node, right_node = root_node.get_children()
            root_node = left_node
        except:
            # print('root node is : ',root_node.get_children())
            left_node, right_node = root_node.get_children()[:2]
            
            # exit(-1)

        left_size = len(left_node.get_leaves())
        right_size = len(right_node.get_leaves())
        # print('root is : : ', root_node.name)

        # print('left size is : ', left_size, ' right size is : ',
            #   right_size, ' need to delete more : ', count)

        p = np.random.uniform(0, 1)

        shouldGoLeft = p < left_size / (left_size + right_size)

        # print('p is : ', p, ' should go left : ', shouldGoLeft)

        if shouldGoLeft:
            if left_size > count:
                # print('going left')
                root_node = left_node
            else:
                ret_taxa += [x.name for x in left_node.get_leaves()]
                count -= left_size
                times_broken += 1
                root_node = right_node
        else:
            if right_size > count:
                # print('going right')
                root_node = right_node
            else:
                ret_taxa += [x.name for x in right_node.get_leaves()]

                count -= right_size
                times_broken += 1
                root_node = left_node

    # print('ret taxa is : ', ret_taxa, len(ret_taxa))
    return save_taxa_from_extinction(ret_taxa)

    # iter = not root_node.is_leaf()

    # print(gt)

    # print('ekhon chole jacchi kintu jacchi nah!')
    # exit(-1)


def get_bounds(range):
    """
    returns the higher and lower bound
    of a range

    both "1-2" or "1"

    returns (l_bound, h_bound)
    """
    # if RANGE_SEPARATOR in range:
    range = range.split(RANGE_SEPARATOR)

    assert len(range) <= 2, range + ' should not be in this form '

    return int(range[0]), int(range[-1])


def remove_taxa_from_gts(range, in_file, out_file):
    '''
    removes range of taxa from each gene tree
    range = "1-3"
    doesn't eliminates a taxa entirely from all gene trees 
    '''
    l_bound, h_bound = get_bounds(range=range)
    print('---------------', 'Pruning started ', in_file, ' ==> ', out_file, '( ', l_bound, '-', h_bound,
          ') ---------------')
    in_time = time.time()

    ###
    # the original one
    # trees = dendropy.TreeList.get_from_path(treeName, 'newick',as_rooted=True,preserve_underscores=True)
    # as_rooted is critically deprecated
    # rooting is our new best friend
    ###
    trees = dendropy.TreeList.get_from_path(src=in_file, schema='newick', rooting='force-rooted',
                                            preserve_underscores=True)

    global taxon_left_count  # dictionary of taxa left count
    taxon_left_count = {}
    taxa_list, gt_list = get_taxa_list_AND_gt_list(in_file)

    for taxa in taxa_list:
        taxon_left_count[taxa] = len(gt_list)
    # find preserved taxa
    # gt = trees[0].__str__()
    # taxa_list = get_taxa_list_from_gt(gt)
    # preserved_taxa_idx = random.randint(0, len(taxa_list) - 1)
    # preserved_taxa = taxa_list[preserved_taxa_idx]

    create_file_abs(out_file)
    with open(out_file, 'w') as f:
        for tree in trees:
            pruned_tree = dendropy.Tree(tree)

            num_deletion = random.randint(l_bound, h_bound)

            ###         gt = tree.as_newick_string()

            gt = tree.__str__()

            # taxon_set = get_deleted_taxa(gt, num_deletion)
            # print('taxon set :', taxon_set)
            # taxon_set = get_deleted_taxa_without_removing_one(gt, num_deletion, preserved_taxa)

            if MISSING_BY_CLADE:
                taxon_set = get_deleted_taxa_by_clade(gt, num_deletion)
            else:
                taxon_set = get_deleted_taxa(gt, num_deletion)

            print('missing taxon set :', taxon_set)
            print('missing taxon set size :', len(taxon_set))

            ###        prTree.prune_taxa_with_labels(taxon_sets, update_splits=True, delete_outdegree_one=True)
            pruned_tree.prune_taxa_with_labels(taxon_set)

            s = pruned_tree.__str__()

            # s = bytes(s, encoding='UTF-8')

            # print(gt, taxon_set, s)

            f.write(s)

            f.write(';\n')

    time_required = int(time.time() - in_time)
    print('---------------', 'Pruning done ', time_required, 's ', in_file, ' ==> ', out_file, '( ', l_bound, '-',
          h_bound, ') ---------------')
