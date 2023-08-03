import time
from ntpath import join
import os
from codes.incomplete_maker import remove_taxa_from_gts


from codes.parameters import ASTRAL, COMPLETE, GENE_TREE, INCOMPLETE, OUTPUT_FOLDER, REMOVED_TAXA_RANGE, INPUT_FOLDER, GENE_TREE_SET_EXTENSION, WORKING_FOLDER

from codes.utils.file import create_parent_dir, dir_exists_abs, file_exists_absolute, join_dir


from codes.utils.file import create_file_abs, create_parent_dir, dir_exists_abs, file_exists_absolute, join_dir
from codes.estimator.wQFM import run_wQFM
from codes.estimator.astral import run_ASTRAL


def gen_incomplete_gts():
    '''
    removes taxa range from gene tree set 
    '''

    for range in REMOVED_TAXA_RANGE:
        for in_file in os.listdir(INPUT_FOLDER):
            # print(in_file)
            if in_file.endswith(GENE_TREE_SET_EXTENSION):
                out_file = join_dir(OUTPUT_FOLDER, INCOMPLETE,
                                    range, GENE_TREE,  in_file)
                print(out_file)
                create_parent_dir(out_file)
                remove_taxa_from_gts(range, join_dir(
                    INPUT_FOLDER, in_file), out_file)


def main():
    o_time = time.time()
    gen_incomplete_gts()

    # run_ASTRAL(INPUT_FOLDER, join_dir(OUTPUT_FOLDER, COMPLETE, 'astral'))
    # run_incomplete_ASTRAL()
    # # return

    # run_wQFM(INPUT_FOLDER, join_dir(OUTPUT_FOLDER, COMPLETE, 'wQFM'))
    # run_incomplete_wQFM()

    # calculate_RF_distance()
    # calculate_Quartet_Score()
    print("\n\n------------------- preprocessor ran in ",
          time.time()-o_time, 's -------------')

    pass


if __name__ == "__main__":
    main()
