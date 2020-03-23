import numpy as np
import matplotlib.pyplot as plt

import sklearn_tools as skt
import babar_tools as bt

import sys
import pickle

infilenames = sys.argv[1:]

allvars,histos = bt.read_in_files_and_combine_all_the_dictionaries(infilenames)

param_labels = list(allvars.keys())

print(param_labels)

toberemoved = ['mup','ep','pp']

cuts_to_use = 1

data = []
param_labels_used = []
for pl in param_labels:
    x = allvars[pl]['values'][cuts_to_use]
    print(pl,len(x))
    if len(x)>0 and pl not in toberemoved:
        print("Adding {0}".format(pl))
        data.append(x)
        param_labels_used.append(pl)


corrcoefs = []
for i in range(len(param_labels_used)):
    corrcoefs.append([])
    for j in range(len(param_labels_used)):
        x = data[i]
        y = data[j]
        corrcoefs[i].append(np.corrcoef(x,y)[0][1])


#data = skt.read_in_pickle_files(infiles)

fig,ax = skt.plot_corr_matrix(corrcoefs,param_labels_used,title='tmp')

##########################################################
# Plot data
plt.figure(figsize=(12,8))
for i,pl in enumerate(param_labels_used):
    plt.subplot(5,5,i+1)
    x = data[i]
    plt.hist(x, color='r', alpha=0.5, bins=50, histtype='stepfilled', density=True)
    plt.xlabel(pl)

plt.tight_layout()


plt.show()
