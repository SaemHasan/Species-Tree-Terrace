#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from codes.parameters import REMOVED_TAXA_RANGE, ASTRAL, INCOMPLETE, COMPLETE, NUMBER_OF_REPLICA


# In[ ]:


number_of_range = len(REMOVED_TAXA_RANGE)


# In[ ]:


df = pd.read_csv('stats/RF.csv', header=None)
# df = df.groupby(by=[0, 1, 2, 3]).mean()
df.head()


# In[ ]:


arr = df.values[:, [0,1,4,2,3]]
arr = np.array(arr)
# arr


# In[ ]:


df2 = pd.read_csv('stats/RF_consensus.csv', header=None)
df2=df2.sort_values(by=[0,1])
df2.head()
consensus_arr = df2.values[:,:]
consensus_arr


# In[ ]:


def consensus_rf_score(replica_no, missing_range):
    val = -1
    for i in range(len(consensus_arr)):
        if consensus_arr[i][0] == replica_no and consensus_arr[i][1] == missing_range:
            val = consensus_arr[i][2]
            break
    return val


# In[ ]:


consensus_rf_score(2, '8-10')


# In[ ]:


METHOD = ASTRAL
PREV_MISSING_RANGE = ""
PREV_REPLICA_NAME = ""


# In[ ]:


CONSENSUS_BETTER = 0
CONSENSUS_WORSE = 0
CONSENSUS_SAME = 0


# In[ ]:


rows, cols = arr.shape
astral_rf_score=0
astral_row_number = -1
terrace_total_RF = 0
terrace_cnt =0
cur_range_cnt = -1
for i in range(rows):
    if arr[i][0] == METHOD and arr[i][1] == COMPLETE:
        print(arr[i][4], "==> Complete --> "+ METHOD + " RF Score : ", arr[i][2])
        continue

    if arr[i][0] == METHOD and arr[i][1] == INCOMPLETE and arr[i][3] != PREV_MISSING_RANGE:
        astral_rf_score = arr[i][2]
        astral_row_number = i
        PREV_MISSING_RANGE = arr[i][3]
        PREV_REPLICA_NAME = arr[i][4]
        terrace_total_RF = 0
        terrace_cnt = 0
        cnt = np.zeros(3, dtype=int)
        cur_range_cnt += 1
        continue

    if arr[i][0] == METHOD and arr[i][1] == INCOMPLETE and arr[i][3] == PREV_MISSING_RANGE and arr[i][4] != PREV_REPLICA_NAME:
        astral_rf_score = arr[i][2]
        astral_row_number = i
        PREV_MISSING_RANGE = arr[i][3]
        PREV_REPLICA_NAME = arr[i][4]
        terrace_total_RF = 0
        terrace_cnt = 0
        cnt = np.zeros(3, dtype=int)
        continue
    

    terrace_total_RF += arr[i][2]
    terrace_cnt += 1
    # print("Missing Range: ", REMOVED_TAXA_RANGE[cur_range_cnt])
    if arr[i][2] < astral_rf_score:
        cnt[0] += 1 # better
    elif arr[i][2] == astral_rf_score:
        cnt[1] += 1 # same
    else:
        cnt[2] += 1 # worse
    
    if (i < rows-1 and arr[i+1][0] == METHOD and arr[i+1][1] == INCOMPLETE) or i == rows-1:
        replica_no = int(arr[astral_row_number][4].split("_")[0])
        sum = cnt[0] + cnt[1] + cnt[2]
        print("Missing Range: ", REMOVED_TAXA_RANGE[cur_range_cnt])
        print("Replica Name: ", arr[astral_row_number][4])
        print("Total Number of Trees in Terrace: ", sum)
        print(f"Number of Trees Better than {METHOD} : ", cnt[0], "\t percentage ; ", cnt[0]/sum*100, "%")
        print(f"Number of Trees Equal to {METHOD} : ", cnt[1], "\t percentage ; ", cnt[1]/sum*100, "%")
        print(f"Number of Trees Worse than {METHOD} : ", cnt[2], "\t percentage ; ", cnt[2]/sum*100, "%")
        print(METHOD+" RF Score : ", astral_rf_score, "\t Terrace avg RF Score: ", terrace_total_RF/terrace_cnt)
        consensus_rf = consensus_rf_score(replica_no, REMOVED_TAXA_RANGE[cur_range_cnt])
        print("Consensus RF Score: ", consensus_rf)
        print("\n\n")
        if consensus_rf != -1:
            if consensus_rf < astral_rf_score:
                CONSENSUS_BETTER += 1
            elif consensus_rf == astral_rf_score:
                CONSENSUS_SAME += 1
            else:
                CONSENSUS_WORSE += 1
        


# In[ ]:


print("Number of Replica where consensus RF Scores Better: ", CONSENSUS_BETTER)
print("Number of Replica where consensus RF Scores Same: ", CONSENSUS_SAME)
print("Number of Replica where consensus RF Scores Worse: ", CONSENSUS_WORSE)

