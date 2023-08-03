import re
def get_taxa_list_from_gt(line:str):
    '''
    line a single gene tree (str)
    '''
    ret = []
    line = line.strip()
    line_split = line.split(',')
    for xl in line_split:
        xl = re.sub('[\(|\)\;]', '', xl)
        ret.append(xl)
    return ret