import numpy as np
import matplotlib.pylab as plt

import babar_tools as bt

import sys

import pickle

import pandas as pd

infilenames = sys.argv[1:]
allvars,histos = bt.read_in_files_and_combine_all_the_dictionaries(infilenames)

# What if we only want from cut 1 on when nbnvbcand == 1?
x = allvars['nbnvbcand']['values'][3] 
idx = x==1

tmp = {}
for key in allvars.keys():

    # Skip the PID flags
    if key.find('Is')>=0:
        continue
    print(key,len(allvars[key]['values'][3]),len(idx))
    tmp[key] = allvars[key]['values'][3][idx]

df = pd.DataFrame.from_dict(tmp)


#df = pd.DataFrame.from_dict(allvars)
#
sp = infilenames[0].split('SP-')[1].split('/')[0]
decay = infilenames[0].split('SP-')[1].split('/')[1]
outname = 'CUT_SUMMARY_SP-{0}_{1}.h5'.format(sp,decay)
#
df.to_hdf(outname,key='df',mode='w')

# Can do stuff like
# sns.distplot(df['tagbcandmass'].values[0][1],norm_hist=False,kde=False,hist_kws={'range':(5,10)})
