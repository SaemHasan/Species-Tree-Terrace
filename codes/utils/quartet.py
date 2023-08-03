def align_quartet(four_taxa):
    '''
    align the taxa and return value also (1, 2, 3)
    ab | cd 
    2 : b < c 
    1 : b < d
    0 : b > c
    four_taxa: str(four taxa)
    '''

    if four_taxa[0] > four_taxa[1]:
        four_taxa[0], four_taxa[1] = four_taxa[1], four_taxa[0]
    if four_taxa[2] > four_taxa[3]:
        four_taxa[2], four_taxa[3] = four_taxa[3], four_taxa[2]

    if four_taxa[0] > four_taxa[2]:
        four_taxa[0], four_taxa[2] = four_taxa[2], four_taxa[0]
        four_taxa[1], four_taxa[3] = four_taxa[3], four_taxa[1]
    
    """ number = 2 
    if four_taxa[1] > four_taxa[3]:
        number = 1
    elif four_taxa[1] > four_taxa[2]:
        number = 0 """

    
    if four_taxa[1] < four_taxa[2]:
        number = 0 
    elif four_taxa[1] < four_taxa[3]:
        number = 1 
    else:
        number = 2 

    return four_taxa, number
    