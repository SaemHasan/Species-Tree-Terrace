import subprocess, os
from codes.utils.file import create_file_abs, dir_exists_abs, file_remove_absolute, join_dir
from codes.parameters import GENE_TREE_SET_EXTENSION, OUTPUT_FOLDER, SCRIPT_FOLDER


def tree_generation_using_Astral(in_file, out_file):	
    create_file_abs(out_file)
    # file_remove_absolute(out_file)
    subprocess.call( ['java','-jar', join_dir(SCRIPT_FOLDER,'astral.5.6.3.jar') , '-i', in_file,'-o',out_file] )
    subprocess.call([join_dir(SCRIPT_FOLDER,  'perl_runner.sh'),out_file, SCRIPT_FOLDER])


def run_ASTRAL(in_dir, out_dir):
    '''
    considers all gene tree extension file in in_dir 
    and runs astral resulting in out_dir
    '''
    assert dir_exists_abs(in_dir), in_dir + ' is not a directory.'
    for in_file in os.listdir(in_dir):
        if in_file.endswith(GENE_TREE_SET_EXTENSION):
            in_file_path = join_dir(in_dir, in_file)
            out_file_path = join_dir(out_dir, in_file.replace(GENE_TREE_SET_EXTENSION, '_species' + GENE_TREE_SET_EXTENSION))
            tree_generation_using_Astral(in_file_path, out_file_path)
