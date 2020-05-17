import numpy as np
import matplotlib.pylab as plt

import babar_tools as bt

import sys

import pickle

import pandas as pd

infilenames = sys.argv[1:]
allvars,histos = bt.read_in_files_and_combine_all_the_dictionaries(infilenames)
df = pd.DataFrame.from_dict(allvars)

sp = infilenames[0].split('SP-')[1].split('/')[0]
decay = infilenames[0].split('SP-')[1].split('/')[1]
outname = 'CUT_SUMMARY_SP-{0}_{1}.h5'.format(sp,decay)

df.to_hdf(outname,key='df',mode='w')

# Can do stuff like
# sns.distplot(df['tagbcandmass'].values[0][1],norm_hist=False,kde=False,hist_kws={'range':(5,10)})
