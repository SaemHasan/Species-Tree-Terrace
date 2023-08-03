import subprocess
import shutil
import time, re, collections, os

import numpy as np
from codes.utils.file import create_file_abs, create_parent_dir, dir_exists_abs, file_exists_absolute, file_remove_absolute, join_dir
from codes.utils.quartet import align_quartet
from codes.parameters import FOUR_TAXA_MAP, NUMPY_ARRAY, OUTPUT_FOLDER, SCRIPT_FOLDER, WORKING_FOLDER

from codes.mappings.taxa import Index_mapping

_TEMP_DIR = join_dir(WORKING_FOLDER, 'gt-handler/')

def get_taxa_list_AND_gt_list(input_file):
    '''
    Reads the GT file and returns all the taxa and gene tree list .
    input_file: str(filename of the GT file)
    returns: list of taxa and list of gene trees
    '''
    taxa_map = {}
    gt_list = []
    with open(input_file, 'r') as f:
        for line in f:
            # we support comment now in  gene trees
            if line.startswith('#'):
                continue
            line = line.strip()
            if line == '':
                continue
            gt_list.append(line)

            line_split = line.split(',')
            for xl in line_split:
                xl = re.sub('[\(|\)\;]', '', xl)
                # xl is a taxa 
                if xl not in taxa_map:
                    taxa_map[xl] = 1
    taxa_list = sorted(list(taxa_map.keys()))
    

    # taxa_map = collections.OrderedDict(sorted(taxa_map.items())) ### why sir do this ? 
    # taxa_list = []
    # for key,value in taxa_map.items():
    #     taxa_list.append(key)
    # for i in range(len(taxa_list)):
    #     assert taxa_list1[i] == taxa_list[i], str(i) + taxa_list1[i] + taxa_list[i] + 'sir thik'

    # print(taxa_list)
    return taxa_list, gt_list

def four_taxa_seq_generator(taxa_map):
    '''
    Generate all possible four taxa sequences.
    taxa_map: list of taxa
    '''
    taxa_list = taxa_map.get_taxa_list()

    seq_list = []
    for i in range(len(taxa_list)):
        for j in range(i+1, len(taxa_list)):
            for k in range(j+1, len(taxa_list)):
                for l in range(k+1, len(taxa_list)):
                    seq_list.append(taxa_list[i] + ',' + taxa_list[j] + ',' + taxa_list[k] + ',' + taxa_list[l])
    
    return seq_list






def get_column_determinator(quartet_list, out_file ):
    '''
    quartet_list: str(quartet_list) 
    output_dir: str(output directory)
    # whole_or_tr_no: int(whole or tr no)
    '''

    output_map = {}
    column_determinator={}
    cnt = 0 
    for quartet in quartet_list:
        # print(quartet)

        taxa = quartet.split(',')
        taxa, num = align_quartet(taxa)
        column_determinator[str(sorted(taxa))] = cnt
        cnt += 1
        output_map[quartet] = cnt
    
    
    # file_remove_absolute(out_file)
    create_file_abs(out_file)
    with open(out_file, "w") as f:
        f.write(str(output_map))
    return column_determinator

def script_run(gt):
    '''
    run the script to generate quartets 
    input_file: str(input file)
    '''
    # script preparation 
    temp_in_file =join_dir(_TEMP_DIR, 'tree_input.tree') # used for sending to script to get quartet table
    temp_out_file = join_dir(_TEMP_DIR, 'output.quartets') # used for script  getting quartet table
    # print('temp_in_file -> ' + temp_in_file)
    with open(temp_in_file, "w") as f:
        f.write(gt) # script read the file 
    # print('--------------------------------------------')
    subprocess.call([join_dir(SCRIPT_FOLDER,  'quartet_controller.sh'), temp_in_file, temp_out_file, SCRIPT_FOLDER])
    # print('--------------------------------------------')
    with open(temp_out_file, "r") as f:
        data = f.read()
        lines = data.split('\n')
        no_quartets = len(lines) - 1 # last line is empty because of split ? 
    return data, lines, no_quartets


def get_gt_index_quartet_table(gt_list, four_taxa_seq, out_file, col_det):
    '''
    populates our necessary quartet table. 
    gt_list: list of gene trees
    taxa_map: Index_mapping

        1, ab|cd ac|bd ad|bc
            1      0    0
        2, ab|cd ac|bd ad|bc
            0      1    0
    '''

    no_gt = len(gt_list)
    # four_taxa_seq=four_taxa_seq_generator(taxa_map)

    table = np.zeros((no_gt, len(four_taxa_seq), 3))

    # out file already exists
    file_remove_absolute(out_file)

    # create the temp dir
    if not  dir_exists_abs(_TEMP_DIR):
        os.makedirs(_TEMP_DIR, exist_ok = True)
    assert dir_exists_abs(_TEMP_DIR), "temp dir not created : " + _TEMP_DIR
    for index, gt in enumerate(gt_list):
        # print("----------------- Working with the tree ", index, "------------------------")

        assert index > -1, "index is negative : " + str(index)
        

        data, lines, no_quartets = script_run(gt)        
        
        for i in range(len(lines)-1):
            
            quartet = lines[i].split(';')[0]
            assert quartet != '', "quartet is empty : " + quartet + ' last line handle '
            taxa = re.sub('[\)\(]', '', quartet).split(',')
            taxa, typ = align_quartet(taxa)
            taxa = sorted(taxa)
            # print('col det ', col_det)
            # if str(taxa) in col_det:
            axis_y = int(col_det[str(taxa)])
            axis_z = int(typ)

            table[index][axis_y][ axis_z] = 1.
            # else:
            #     print(taxa , ' is not present. why ? --------------------------------')
            #     exit(1)
        
        # print("-----------------Done Working with the tree ", index, "------------------------")


        
        # break
    # clear the directory   


    create_file_abs(out_file)
    np.save(out_file, table, allow_pickle=True,fix_imports=True)
    shutil.rmtree(_TEMP_DIR)



def gt_read_and_process(input_file, out_dir, file_name, map_file_name):
    print("============= Starting file -> " + input_file + "===================")    		
    in_time = time.time()
    
    taxa_list, gt_list=get_taxa_list_AND_gt_list(input_file)

    # taxa_map should be updated here
    taxa_map = Index_mapping(taxa_list)
    four_taxa_seq = four_taxa_seq_generator(taxa_map)

    assert os.path.isabs(map_file_name) == False, "please provide only file name not absolute path " + map_file_name

    col_det = get_column_determinator(four_taxa_seq, join_dir(out_dir, FOUR_TAXA_MAP,  map_file_name))

    assert os.path.isabs(file_name) == False, "please provide only file name not absolute path " + file_name
    get_gt_index_quartet_table(gt_list, four_taxa_seq, join_dir(out_dir, NUMPY_ARRAY, file_name) , col_det)

    

    print("Time Required -> ", time.time()-in_time)
    print("=============== done with file -> " + input_file + "================")


def main():
    pass

if __name__ == '__main__':
    main()