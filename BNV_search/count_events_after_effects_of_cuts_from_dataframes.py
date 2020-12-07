import numpy as np

import plotting_tools as pt

import pandas as pd

import sys


infilenames = sys.argv[1:]


sptag = pt.get_sptag(infilenames[0])
print(sptag)

tot = 0
for infilename in infilenames:
    df = pd.read_hdf(infilename)
    size = len(df)
    tot += size
    #print(tot,size)

print(sptag[0],'\tTotal: ',tot)

