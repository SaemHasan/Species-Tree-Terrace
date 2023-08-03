import subprocess
import csv
from doctest import OutputChecker
from operator import gt, truediv
from re import sub
from tabnanny import check
import numpy as np
import time
import ast
from ntpath import join
import os
from codes.incomplete_maker import remove_taxa_from_gts

from codes.parameters import ASTRAL, NUMPY_EXTENSION, QUARTETS, SCRIPT_FOLDER, STATS_FOLDER, TRUE_FOLDER, WQFM, \
    COMPLETE, GENE_TREE, QUARTETS, INCOMPLETE, IMPUTED_LIST, OUTPUT_FOLDER, NUMPY_ARRAY, REMOVED_TAXA_RANGE, INPUT_FOLDER, \
    QUARTETS_EXTENSION, MODES_LIST, WORKING_FOLDER, METHODS

from codes.utils.file import create_file_abs, create_parent_dir, dir_exists_abs, file_exists_absolute, join_dir
from codes.estimator.wQFM import run_wQFM
from codes.estimator.astral import run_ASTRAL


def run_incomplete_wQFM():
    """
    runs wQFM in all the incomplete folders
    """

    for range in REMOVED_TAXA_RANGE:
        root_dir = join_dir(OUTPUT_FOLDER, INCOMPLETE, range)
        in_dir = join_dir(root_dir, GENE_TREE)
        out_dir = join_dir(OUTPUT_FOLDER, INCOMPLETE, range, WQFM)
        assert dir_exists_abs(in_dir), in_dir + \
            " doesn't exist. please run the previous steps"

        run_wQFM(in_dir, out_dir)


def generate_quartets_from_imputed_npy():
    Root_Folder = os.getcwd()

    for _IMPUTED in IMPUTED_LIST:

        for doing in REMOVED_TAXA_RANGE:

            Imputed_Folder = join_dir(WORKING_FOLDER, _IMPUTED, doing)
            Quartets_Folder = join_dir(
                OUTPUT_FOLDER, _IMPUTED, doing, QUARTETS)
            Map_Folder = join_dir(OUTPUT_FOLDER, INCOMPLETE, doing, 'map')

            os.makedirs(Quartets_Folder, exist_ok=True)

            for file_ in os.listdir(Imputed_Folder):
                print(file_)
                if not file_.endswith('.npy'):
                    continue
                # assuming that the gene trees are labelled with a [NUMBER]_* format
                cnt = file_.split("_")[0]

                print(file_, cnt)
                qt_file = file_.replace(NUMPY_EXTENSION, QUARTETS_EXTENSION)
                mp_file = file_.replace(NUMPY_EXTENSION, '.mp')
                with open(join_dir(Map_Folder, mp_file), 'r') as mp:
                    quartet_idx_map = ast.literal_eval(mp.read())
                    idx_quartet_map = {v: k.split(',')
                                       for k, v in quartet_idx_map.items()}
                    idx_config_map = {k: [0, 0, 0]
                                      for k in idx_quartet_map.keys()}

                imp = np.load(join_dir(Imputed_Folder, file_))
                assert imp.shape[2] == 3
                for i in range(imp.shape[0]):
                    for j in range(imp.shape[1]):
                        for k in range(imp.shape[2]):
                            if imp[i][j][k] == 1:
                                idx_config_map[j + 1][k] += 1

                with open(join_dir(Quartets_Folder, qt_file), 'w') as qt:
                    for key in idx_quartet_map.keys():
                        a, b, c, d = idx_quartet_map[key]
                        print('((' + a + ',' + b + '),(' + c + ',' + d +
                              ')); ' + str(idx_config_map[key][0]), file=qt)
                        print('((' + a + ',' + c + '),(' + b + ',' + d +
                              ')); ' + str(idx_config_map[key][1]), file=qt)
                        print('((' + a + ',' + d + '),(' + b + ',' + c +
                              ')); ' + str(idx_config_map[key][2]), file=qt)


def run_imputed_wQFM():
    '''
    runs wQFM in all the imputed folders
    '''
    try:
        generate_quartets_from_imputed_npy()
    except FileExistsError as e:
        pass

    for _IMPUTED in IMPUTED_LIST:
        for range in REMOVED_TAXA_RANGE:
            root_dir = join_dir(OUTPUT_FOLDER, _IMPUTED, range)
            in_dir = join_dir(root_dir, QUARTETS)
            out_dir = join_dir(root_dir, WQFM)
            assert dir_exists_abs(in_dir), in_dir + \
                " doesn't exist. please run the previous steps"

            run_wQFM(in_dir, out_dir)
            print('hello')


def calculate_RF_distance():
    true_tree = join_dir(TRUE_FOLDER, 'true-species.out.tree')
    out_dir = STATS_FOLDER

    csv_out_list = []

    for mode in MODES_LIST:
        for est in (WQFM, ASTRAL):
            if est == ASTRAL and mode in IMPUTED_LIST:
                continue
            RR = [''] if mode == COMPLETE else REMOVED_TAXA_RANGE
            for range in RR:
                in_dir = join_dir(OUTPUT_FOLDER, mode, range, est)
                # print(range, in_dir)
                for file_ in os.listdir(in_dir):
                    if (file_.endswith('.tre' if est == WQFM else '.out.tre')):
                        file_abs = join_dir(in_dir, file_)
                        result = ast.literal_eval(
                            subprocess.check_output(['getFpFn.py', '-t', true_tree, '-e', file_abs], encoding='UTF-8'))
                        assert result[0] == result[1] == result[2]
                        dist = str(result[0])
                        print(est, mode, range, file_, dist)
                        csv_out_list += [(est, mode, range, file_, dist)]

    stat_fl = 'stats/RF.csv'
    with open(stat_fl, 'a') as stat_file:
        csv.writer(stat_file).writerows(csv_out_list)


def split_token_and_send_Qscore(stderr):
    # SSMA
    stderr = stderr.decode('UTF-8')

    if not "Final quartet" in stderr:
        print("Problem !!!!!!!")
        print(stderr)
        print("Problem !!!!!!!")

    for item in stderr.split("\n"):
        if "Final quartet" in item:
            score = item.strip().split(":")[1].strip()
            # print(score)
            return score


def calculate_Quartet_Score():
    # true_tree = join_dir(TRUE_FOLDER, 'true-species.out.tree')
    # out_dir = STATS_FOLDER

    csv_out_list = []

    gene_trees_dir = INPUT_FOLDER
    # species_trees_dir = join_dir(OUTPUT_FOLDER, COMPLETE, ASTRAL)

    try:
        # print(in_dir, OUTPUT_FOLDER)
        for mode in MODES_LIST:
            for est in METHODS:
                RR = [''] if mode == COMPLETE else REMOVED_TAXA_RANGE
                for range in RR:
                    species_trees_dir = join_dir(OUTPUT_FOLDER, mode, range, est)
                    # print(range, in_dir)
                    for file_ in os.listdir(species_trees_dir):
                        if (file_.endswith('.tre' if est == WQFM else '.out.tre')):
                            st_file_abs = join_dir(species_trees_dir, file_)
                            file_ = file_.replace("_species", "").replace(
                                ".out", "").replace(".tre.tre", ".tre")
                            gt_file_abs = join_dir(gene_trees_dir, file_)
                            # print(st_file_abs, gt_file_abs)
                            stdout, stderr = subprocess.Popen(
                                ['java', '-jar', join_dir(SCRIPT_FOLDER, 'astral.5.6.3.jar'), '-q', st_file_abs, '-i',
                                 gt_file_abs], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False).communicate()
                            q_score = split_token_and_send_Qscore(stderr)
                            csv_out_list += [(est, mode, range,
                                              file_, q_score)]
                                              

        for file_ in os.listdir(gene_trees_dir):
            gt_file_abs = join_dir(gene_trees_dir, file_)
            st_file_abs = join_dir(TRUE_FOLDER, 'true-species.out.tree')
            # print(st_file_abs, gt_file_abs)
            stdout, stderr = subprocess.Popen(
                ['java', '-jar', join_dir(SCRIPT_FOLDER, 'astral.5.6.3.jar'),
                 '-q', st_file_abs, '-i', gt_file_abs],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False).communicate()
            # print(stderr)
            q_score = split_token_and_send_Qscore(stderr)
            csv_out_list += [('TRUE', '', '', file_, q_score)]
    except:
        pass

    with open('stats/QS.csv', 'a') as stat_file:
        csv.writer(stat_file).writerows(csv_out_list)


def convert_to_wQMC_format():
    in_folder = INPUT_FOLDER
    """ for file_ in os.listdir(in_folder):
        if file_.endswith('.qrts'):
            subprocess.call(['python', join_dir(SCRIPT_FOLDER, 'newick_to_wqmc_converter.py'), join_dir(in_folder, file_)])
 """
    for range in REMOVED_TAXA_RANGE:
        in_folder = join_dir(OUTPUT_FOLDER, INCOMPLETE, range, 'gt')
        for file_ in os.listdir(in_folder):
            if file_.endswith('.qrts'):
                subprocess.call(
                    ['python', join_dir(SCRIPT_FOLDER, 'newick_to_wqmc_converter.py'), join_dir(in_folder, file_)])


def run_incomplete_ASTRAL():
    '''
    runs astral in all the incomplete folders
    '''
    for range in REMOVED_TAXA_RANGE:
        root_dir = join_dir(OUTPUT_FOLDER, INCOMPLETE, range)
        in_dir = join_dir(root_dir, GENE_TREE)
        out_dir = join_dir(OUTPUT_FOLDER, INCOMPLETE, range, ASTRAL)
        assert dir_exists_abs(in_dir), in_dir + \
            " doesn't exist. please run the previous steps"

        run_ASTRAL(in_dir, out_dir)


def main():
    # astral
    run_ASTRAL(INPUT_FOLDER, join_dir(OUTPUT_FOLDER, COMPLETE, 'astral'))
    # run_incomplete_ASTRAL()
    # return

    # run_wQFM(INPUT_FOLDER, join_dir(OUTPUT_FOLDER, COMPLETE, 'wQFM'))
    # run_incomplete_wQFM()
    # run_imputed_wQFM()
    # calculate_RF_distance()
    # calculate_Quartet_Score()
    # convert_to_wQMC_format()


if __name__ == '__main__':
    main()
    # generate_quartets_from_imputed_npy()
