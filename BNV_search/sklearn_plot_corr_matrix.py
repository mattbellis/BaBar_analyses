import numpy as np
import matplotlib.pyplot as plt

import sklearn_tools as skt
import babar_tools as bt

import sys
import pickle

import pandas as pd

infilenames = sys.argv[1:]

IS_PICKLE_FILES = False

toberemoved = ['mup','ep','pp']

##########################################################
if IS_PICKLE_FILES:
    allvars,histos = bt.read_in_files_and_combine_all_the_dictionaries(infilenames)

    param_labels = list(allvars.keys())

    print(param_labels)

    cuts_to_use = 1
###
else:
    df = pd.read_csv(infilenames[0])

    param_labels = df.columns.values

    allvars = df.values

data = []
param_labels_used = []

for i,pl in enumerate(param_labels):
    if IS_PICKLE_FILES:
        x = allvars[pl]['values'][cuts_to_use]
    else:
        x = allvars[i]

    print(pl,len(x))
    print(type(x))
    print(len(x[x!=x]))
    if len(x)>0 and pl not in toberemoved:
        print("Adding {0}".format(pl))
        if i==0:
            mask = x==x
        else:
            mask *= x==x
        data.append(x)
        param_labels_used.append(pl)

################################################################################

corrcoefs = []
for i in range(len(param_labels_used)):
    corrcoefs.append([])
    for j in range(len(param_labels_used)):
        print(param_labels_used[i], param_labels_used[j])
        x = data[i][mask]
        y = data[j][mask]
        corrcoefs[i].append(np.corrcoef(x,y)[0][1])


#data = skt.read_in_pickle_files(infiles)

#tag = "SP_9456_pmu"
#tag = "SP_1235_1237_pmu"
#tag = "SP_1005_pmu"
#tag = "SP_998_pmu"

#tag = "SP_11975_pnu"
#tag = "SP_1235_1237_pnu"
#tag = "SP_1005_pnu"
#tag = "SP_998_pnu"

#tag = "SP_11976_nmu"
#tag = "SP_1235_1237_nmu"
#tag = "SP_1005_nmu"
tag = "SP_998_nmu"

fig,ax = skt.plot_corr_matrix(corrcoefs,param_labels_used,title='')
plt.savefig("corr_matrix_"+tag+".png")

##########################################################
# Plot data
plt.figure(figsize=(12,8))
for i,pl in enumerate(param_labels_used):

    prange=None
    if pl=="bnvbcandmass":
        prange = (5.0,6.5)
    elif pl=="bnvbcandMES":
        prange = (5.2,5.3)
    elif pl=="bnvbcandDeltaE":
        prange = (-0.3,0.3)
    elif pl=="tagbcandmass":
        prange = (0.0,10.0)
    elif pl=="tagbcandMES":
        prange = (5.0,5.3)
    elif pl=="tagbcandDeltaE":
        prange = (-3.0,6.0)
    elif pl.find('p3')>=0:
        prange = (0,4)
    elif pl=="missingmass":
        prange = (-5.0,10.0)
    elif pl=="missingmom":
        prange = (0.0,5.0)
    elif pl=="missingE":
        prange = (-5.0,5.0)
    elif pl=="scalarmomsum":
        prange = (5.0,15.0)
    elif pl.find('r2')>=0 or pl.find('sphericity')>=0 or pl.find('thrust')>=0:
        prange = (0,1)
    elif pl.find('nphot')>=0 or pl.find('nchar')>=0:
        prange = (0,22)

    plt.subplot(6,5,i+1)
    x = data[i][mask]
    #plt.hist(x, color='r', alpha=0.5, bins=50, histtype='stepfilled', density=True)
    plt.hist(x, color='r', alpha=0.5, bins=50, range=prange, histtype='stepfilled', density=False)
    plt.xlabel(pl)

plt.tight_layout()
plt.savefig("corr_matrix_vars_"+tag+".png")


plt.show()
