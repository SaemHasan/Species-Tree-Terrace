from ntpath import join
from re import sub
import subprocess
import os
from codes.utils.file import create_file_abs, dir_exists_abs, file_remove_absolute, join_dir
from codes.parameters import GENE_TREE_SET_EXTENSION, QUARTETS_EXTENSION, OUTPUT_FOLDER, SCRIPT_FOLDER, SCRIPT_FOLDER_DEPTH, WORKING_FOLDER


def tree_generation_using_wQFM(in_file, out_file, gene_trees=True):
    create_file_abs(out_file)
    # file_remove_absolute(out_file)
    wd = '/'.join(['..'] * SCRIPT_FOLDER_DEPTH)
    os.chdir(SCRIPT_FOLDER)
    if gene_trees:
        subprocess.call(['java', '-jar', join_dir(SCRIPT_FOLDER, 'wQFM-v1.4.jar'), '-i',
                        join_dir(wd, in_file), '-o', join_dir(wd, out_file), '-im', 'gene-trees'])
    else:
        subprocess.call(['java', '-jar', join_dir(SCRIPT_FOLDER, 'wQFM-v1.4.jar'),
                        '-i', join_dir(wd, in_file), '-o', join_dir(wd, out_file)])
    os.chdir(wd)
    #subprocess.call(['cp', join_dir(SCRIPT_FOLDER, 'input-wqrts-for-jar.wqrts'), join_dir(WORKING_FOLDER, in_file)])


def run_wQFM(in_dir, out_dir):
    '''
    considers all gene tree extension file in in_dir 
    and runs astral resulting in out_dir
    '''
    assert dir_exists_abs(in_dir), in_dir + ' is not a directory.'
    for in_file in os.listdir(in_dir):
        if in_file.endswith(GENE_TREE_SET_EXTENSION):
            in_file_path = join_dir(in_dir, in_file)
            out_file_path = join_dir(out_dir, in_file.replace(
                GENE_TREE_SET_EXTENSION, '_species' + GENE_TREE_SET_EXTENSION))
            print(in_file_path, out_file_path)
            tree_generation_using_wQFM(
                in_file_path, out_file_path, gene_trees=True)
            try:
                subprocess.call(['cp', join_dir(SCRIPT_FOLDER, 'input-wqrts-for-jar.wqrts'),
                                join_dir(WORKING_FOLDER, in_file_path + '.qrts')])
                print('Should be copied: ', join_dir(
                    WORKING_FOLDER, in_file_path + '.qrts'))
            except:
                print('Could not copy input_jar.wqrts')

        if in_file.endswith(QUARTETS_EXTENSION):
            in_file_path = join_dir(in_dir, in_file)
            out_file_path = join_dir(out_dir, in_file.replace(
                QUARTETS_EXTENSION, '_species' + GENE_TREE_SET_EXTENSION))
            print(in_file_path, out_file_path)
            tree_generation_using_wQFM(
                in_file_path, out_file_path, gene_trees=False)
