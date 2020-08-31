import sys

import matplotlib.pylab as plt
import numpy as np
import sys
import pandas as pd
import seaborn as sns

import plotting_tools as pt
import babar_dataframe_tools as bd

#df = pd.read_hdf("CUT_SUMMARY_SP-9456_pmu.h5")
df = pd.read_hdf(sys.argv[1])

all_variables = [#'nbnvbcand', \
                'bnvbcandmass', \
                'bnvbcandMES', \
                'bnvbcandDeltaE', \
                'bnvprotp3', \
                'bnvlepp3', \
                'tagbcandmass', \
                'tagbcandMES', \
                'tagbcandDeltaE', \
                'tagq', \
                'missingmass', \
                'missingmom', \
                'missingE', \
                'scalarmomsum', \
                'nhighmom', \
                'np', \
                'nmu', \
                'ne', \
                #'pp', \
                #'mup', \
                #'ep', \
                'r2',  \
                'r2all', \
                'thrustmag', \
                'thrustmagall', \
                'thrustcosth', \
                'thrustcosthall', \
                'sphericityall', \
                'ncharged', \
                'nphot']

# HOW DO WE ONLY WORK WITH THE UNCOMMENTED VARIABLES?

# heatmap
corr = df.corr()

ax = sns.heatmap( corr, vmin=-1, vmax=1, center=0, cmap=sns.diverging_palette(20, 220, n=200), square=True)
ax.set_xticklabels( ax.get_xticklabels(), rotation=45, horizontalalignment='right');

# corr matrix
f = plt.figure(figsize=(10, 8))
plt.matshow(df.corr(), fignum=f.number)
plt.yticks(range(df.shape[1]), df.columns, fontsize=10)
plt.xticks(range(df.shape[1]), df.columns, fontsize=10, rotation=45)
cb = plt.colorbar()
plt.clim(-1,1)
cb.ax.tick_params(labelsize=10)


# plot variables 
fig, axes = plt.subplots(len(df.columns)//4, 4, figsize=(12, 48))

i = 0
for xx in axes:
    for axis in xx:
        df.hist(column = df.columns[i], density=True, bins = 200, ax=axis)
        i = i+1


plt.show()
