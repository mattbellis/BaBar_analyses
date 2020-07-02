import sys
import pandas as pd

outfilename = sys.argv[1]

infilenames = sys.argv[2:]

frames = []
for infilename in infilenames:

    print(infilename)

    df = pd.read_hdf(infilename)

    frames.append(df)


df_merged = pd.concat(frames)

df_merged.to_hdf(outfilename,key='df',mode='w')

