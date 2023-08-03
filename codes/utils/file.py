from genericpath import exists
import os
import shutil

def join_dir(first, *second):
    '''
    Join two directories.
    first: str
    *second: str list 
    '''
    ret = first
    for folder in second:
        if folder == '':
            continue 
        ret = os.path.join(ret, folder)
    return ret


def file_exists_current(file_name):
    '''
    Check if a file exists.
    '''
    return os.path.isfile(join_dir(os.get_cwd(), file_name))


def file_exists_absolute(abs_file_name):
    '''
    Check if a file exists.
    '''
    return os.path.isfile(abs_file_name)

def dir_exists_abs(abs_dir_name):
    '''
    Check if a directory exists.
    '''
    return os.path.isdir(abs_dir_name)


def file_remove_current(cur_file_name):
    '''
    Remove a file.
    '''
    if file_exists_current(cur_file_name):
        os.remove(join_dir(os.get_cwd(), cur_file_name))

def file_remove_absolute(abs_file_name):

    if file_exists_absolute(abs_file_name):
        os.remove(abs_file_name)



def create_parent_dir(file_name):
    '''
    creates the file if it doesn't exist
    or does nothing 
    '''
    os.makedirs(os.path.dirname(file_name), exist_ok=True)


def create_file_abs(abs_file_name):
    '''
    creates a file. 
    removes previous one.
    creates parent directory.
    '''
    file_remove_absolute(abs_file_name)
    create_parent_dir(abs_file_name)

def remove_dir_abs(abs_dir_name):
    '''
    removes a directory. 
    '''
    if dir_exists_abs(abs_dir_name):
        shutil.rmtree(abs_dir_name)

def remove_dir_current(cur_dir_name):
    '''
    removes a directory. 
    '''
    if dir_exists_abs(cur_dir_name):
        # remove non empty directory
        shutil.rmtree(cur_dir_name)

def copy_file_abs(from_file, to_file):
    '''
    copies a file. 
    '''
    shutil.copyfile(from_file, to_file)

def copy_file_current(from_file, to_file):
    '''
    copies a file. 
    '''
    # relative to current directory
    shutil.copyfile(join_dir(os.getcwd(), from_file), join_dir(os.getcwd(), to_file))

def create_dir_current(cur_dir_name):
    '''
    creates a directory. 
    '''
    os.makedirs(cur_dir_name, exist_ok=True)

    