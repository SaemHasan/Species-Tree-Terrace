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

from codes.utils.file import create_file_abs, create_parent_dir, dir_exists_abs, file_exists_absolute, join_dir
from codes.parameters import ASTRAL, NUMPY_EXTENSION, QUARTETS, SCRIPT_FOLDER, STATS_FOLDER, TRUE_FOLDER, WQFM, \
    COMPLETE, GENE_TREE, QUARTETS, INCOMPLETE, IMPUTED_LIST, OUTPUT_FOLDER, NUMPY_ARRAY, REMOVED_TAXA_RANGE, INPUT_FOLDER, \
    QUARTETS_EXTENSION, MODES_LIST, WORKING_FOLDER, METHODS, TERRACE_OUTPUT_FOLDER



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

def calculate_Quartet_Score_for_Terraces(terrace_file_path, gt_file_abs):
    #read terrace file line by line
    #for each line, run ASTRAL and get the score
    csv_out_list = []

    if file_exists_absolute(terrace_file_path):
        with open(terrace_file_path, "r") as f:
            lines = f.readlines()
            number_of_terrace_print_in_file = False
            if "Terrace" in lines[0]:
                number_of_terrace_print_in_file = True
            if number_of_terrace_print_in_file and len(lines) <=2:
                return None
            elif not number_of_terrace_print_in_file and len(lines) <=1:
                return None

            for i, line in enumerate(lines):
                if ( number_of_terrace_print_in_file and i!=0 ) or (not number_of_terrace_print_in_file):
                    tmp_file = open("tmp.txt", "w")
                    print(line, file=tmp_file)
                    tmp_file.close()
                    st_file_abs = join_dir("tmp.txt")
                    # run ASTRAL
                    stdout, stderr = subprocess.Popen(['java', '-jar', join_dir(SCRIPT_FOLDER, 'astral.5.6.3.jar'), '-q', st_file_abs, '-i',gt_file_abs], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False).communicate()
                    q_score = split_token_and_send_Qscore(stderr)
                    # print(q_score)
                    csv_out_list += [('Terrace st no: ', i, '', line, q_score)]
        return csv_out_list            
    else:
        print("Terrace File does not exist: ", terrace_file_path)
        return None

def calculate_Quartet_Score():
    # true_tree = join_dir(TRUE_FOLDER, 'true-species.out.tree')
    # out_dir = STATS_FOLDER

    csv_out_list = []

    complete_gene_trees_dir = INPUT_FOLDER # complete gt folder
    gene_trees_dir = join_dir(OUTPUT_FOLDER, INCOMPLETE) # missing gt folder
    # species_trees_dir = join_dir(OUTPUT_FOLDER, COMPLETE, ASTRAL)

    try:
        # print(in_dir, OUTPUT_FOLDER)
        for mode in MODES_LIST:
            for est in METHODS:
                RR = [''] if mode == COMPLETE else REMOVED_TAXA_RANGE
                for range in RR:
                    species_trees_dir = join_dir(OUTPUT_FOLDER, mode, range, est)
                    # print(range, species_trees_dir)
                    for file_ in os.listdir(species_trees_dir):
                        if (file_.endswith('.tre' if est == WQFM else '.out.tre')):
                            st_file_abs = join_dir(species_trees_dir, file_)
                            file_ = file_.replace("_species", "").replace(
                                ".out", "").replace(".tre.tre", ".tre")
                            if mode == COMPLETE:
                                gt_file_abs = join_dir(complete_gene_trees_dir, file_)
                            else:        
                                gt_file_abs = join_dir(gene_trees_dir, range, GENE_TREE, file_) # missing gt file
                            # print(mode,st_file_abs, gt_file_abs)
                            stdout, stderr = subprocess.Popen(
                                ['java', '-jar', join_dir(SCRIPT_FOLDER, 'astral.5.6.3.jar'), '-q', st_file_abs, '-i',
                                 gt_file_abs], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False).communicate()
                            q_score = split_token_and_send_Qscore(stderr)
                            csv_out_list += [(est, mode, range,
                                              file_, q_score)]
                            
                            if mode == COMPLETE:
                                continue
                            terrace_file_name = range + ".txt"
                            terrace_file_path = join_dir(TERRACE_OUTPUT_FOLDER, terrace_file_name)
                            output = calculate_Quartet_Score_for_Terraces(terrace_file_path, gt_file_abs)
                            if output is not None:
                                csv_out_list += output

                                              
        '''
        for file_ in os.listdir(complete_gene_trees_dir):
            gt_file_abs = join_dir(complete_gene_trees_dir, file_)
            st_file_abs = join_dir(TRUE_FOLDER, 'true-species.out.tree')
            # print(st_file_abs, gt_file_abs)
            stdout, stderr = subprocess.Popen(
                ['java', '-jar', join_dir(SCRIPT_FOLDER, 'astral.5.6.3.jar'),
                 '-q', st_file_abs, '-i', gt_file_abs],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False).communicate()
            # print(stderr)
            q_score = split_token_and_send_Qscore(stderr)
            csv_out_list += [('TRUE', '', '', file_, q_score)] '''
    except:
        pass

    with open('stats/QS.csv', 'w') as stat_file:
        csv.writer(stat_file).writerows(csv_out_list)
        stat_file.close()

def calculate_QuartetScore_for_ST(st_file_abs, gt_file_abs):
    # print(mode,st_file_abs, gt_file_abs)
    stdout, stderr = subprocess.Popen(
         ['java', '-jar', join_dir(SCRIPT_FOLDER, 'astral.5.6.3.jar'), '-q', st_file_abs, '-i', 
          gt_file_abs], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False).communicate()
    q_score = split_token_and_send_Qscore(stderr)

    return q_score


def main():
    calculate_Quartet_Score()
    # calculate_Quartet_Score_for_Terraces(join_dir(TERRACE_OUTPUT_FOLDER, '27-28.txt'), join_dir(OUTPUT_FOLDER, INCOMPLETE,"27-28","gt", '1_gt.tre'))

if __name__ == '__main__':
    main()