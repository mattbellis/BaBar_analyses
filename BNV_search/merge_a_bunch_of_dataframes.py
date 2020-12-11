import sys
import pandas as pd

#outfilename = sys.argv[1]

infilenames = sys.argv[1:]

sp = 'default'
decay = 'default'
outfilename = 'CUT_SUMMARY_SP-{0}_{1}.h5'.format(sp,decay)
if infilenames[0].find('SP-')>=0:
    sp = infilenames[0].split('SP-')[1].split('/')[0]
    decay = infilenames[0].split('SP-')[1].split('/')[1]
    outfilename = 'CUT_SUMMARY_SP-{0}_{1}.h5'.format(sp,decay)
elif infilenames[0].find('AllEvents-')>=0:
    sp = infilenames[0].split('AllEvents-')[1].split('-')[0]
    decay = infilenames[0].split('AllEvents')[1].split('/')[1]
    outfilename = 'CUT_SUMMARY_AllEvents-{0}_{1}.h5'.format(sp,decay)

print(outfilename)
#exit()

frames = []
nfiles = len(infilenames)
for i,infilename in enumerate(infilenames):

    if i%100==0:
        print(i,nfiles,infilename)

    df = pd.read_hdf(infilename)
    print(len(df))

    frames.append(df)


df_merged = pd.concat(frames)

df_merged.to_hdf(outfilename,key='df',mode='w')

