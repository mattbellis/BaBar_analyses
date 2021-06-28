import sys
import pandas as pd

import babar_dataframe_tools as bd

outfilename = sys.argv[1]

infilenames = sys.argv[2:]

frames = []
nfiles = len(infilenames)
for i,infilename in enumerate(infilenames):

    if i%100==0:
        print(i,nfiles,infilename)

    df = pd.read_hdf(infilename)
    print(i,len(df),nfiles,infilename)

    frames.append(df)


df_merged = pd.concat(frames)

df_merged.to_hdf(outfilename,key='df',mode='w')

