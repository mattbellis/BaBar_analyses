import sys
import pandas as pd

#outfilename = sys.argv[1]

infilenames = sys.argv[1:]

sp = infilenames[0].split('SP-')[1].split('/')[0]
decay = infilenames[0].split('SP-')[1].split('/')[1]
outfilename = 'CUT_SUMMARY_SP-{0}_{1}.h5'.format(sp,decay)

frames = []
for infilename in infilenames:

    print(infilename)

    df = pd.read_hdf(infilename)

    frames.append(df)


df_merged = pd.concat(frames)

df_merged.to_hdf(outfilename,key='df',mode='w')

