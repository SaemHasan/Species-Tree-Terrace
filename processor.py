#!/usr/bin/env python
# coding: utf-8

# In[17]:


# !mkdir in
# !cp dataset/taxa-37/gene-tree/noscale.200g.500b/1_gt.tre in/


# In[18]:


# !python preprocessor.py > /dev/null
# !python postprocessor.py > /dev/null


# In[ ]:





# In[19]:


import  numpy  as  np


# In[ ]:





# In[20]:


def getTaxaSet(t):
    return t.replace('(', '').replace(')', '').split(';')[0].split(':')[0].split(',')


# In[21]:


METHOD = 'wQFM'
OUTGROUP = 'GAL'

st = open('input.nwk')
st = st.read()
gts = open('gt.tre')

gts = gts.read().split(';\n')[:-1] 

# print(len(gts))

# print(st)
taxaSet = getTaxaSet(st)
# print(taxaSet)
matrix = np.zeros((len(taxaSet), len(gts)), dtype=int)


# print(len(gts))
for gt_idx, gt in  enumerate(gts) :
    # print(gt)
    cur_taxaSet = getTaxaSet(gt)
    # print(cur_taxaSet)
    for i, tx in enumerate(taxaSet):
        if tx  in cur_taxaSet or tx == OUTGROUP:
            matrix[i][gt_idx] = 1


# In[ ]:





# In[22]:


# print(matrix)


# In[23]:


with open('input.data', 'w', newline='') as f:
    print(matrix.shape[0], matrix.shape[1], file=f)
    for i in range(len(taxaSet)):
    
        # f.write(matrix[i].tostring(), taxaSet[i])
        print(*matrix[i],taxaSet[i], end='\n', file=f)


# In[24]:


# !dir
# cp 'out/incomplete/20-22/astral/1_gt_species.out.tre' 'valo.nwk' 


# In[ ]:




