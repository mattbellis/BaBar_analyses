import sys
import pandas as pd

import babar_dataframe_tools as bd

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

    # To merge all the data files
    #decay = infilenames[0].split('_')[-1].split('.')[0]
    ##outfilename = 'CUT_SUMMARY_AllEvents-MERGED_{0}_{1}.h5'.format('AllRuns',decay)
    #outfilename = 'CUT_SUMMARY_AllEvents-MERGED_{0}_WITHBNVCHILDRENPCUT_{1}.h5'.format('AllRuns',decay)

print(outfilename)
print("-------------")
#exit()

frames = []
nfiles = len(infilenames)
for i,infilename in enumerate(infilenames):

    if i%100==0:
        print(i,nfiles,infilename)

    df = pd.read_hdf(infilename)
    print(i,len(df),nfiles,infilename)

    #bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') 
    #bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='electron')
    #bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='electron')


    #frames.append(df[bnv_children_momentum_mask])
    frames.append(df)


df_merged = pd.concat(frames)

df_merged.to_hdf(outfilename,key='df',mode='w')

