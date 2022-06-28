import pandas as pd
import sys
import numpy as np

import babar_dataframe_tools as bdtools

#np.random.seed(0)

infilename = sys.argv[1]
print("------------------")
print(infilename)

decays = ['pmu','pe','pnu','nmu','ne']
for d in decays:
    if infilename.find(d)>=0:
        decay = d
        break

print(f"This is for {decay}")

nentries_to_grab = int(sys.argv[2])

DUMP_OPPOSITES = True
if len(sys.argv)>3:
    DUMP_OPPOSITES = bool(sys.argv[3])

df_org = pd.read_hdf(infilename)

print("Org entries: {0}".format(len(df_org)))

mask = bdtools.decay_specific_cuts(df_org,decay=decay)

#df = df_org.sample(n=nentries_to_grab)
nvals = len(df_org[mask])

df_org = df_org[mask]
#print(len(df_org))

print(f"{nvals} pass the mask")

if nentries_to_grab>nvals:
    nentries_to_grab = nvals

idx = np.random.choice(np.arange(0,nvals),nentries_to_grab,replace=False)

#print(idx)

allidx = np.arange(0,nvals)
notidx = np.setdiff1d(allidx,idx)
#
df = df_org.iloc[idx]
if DUMP_OPPOSITES:
    df_alt = df_org.iloc[notidx]
print(f"Creating a sample of {len(df)} and an OPPOSITE sample of {len(df_alt)}")
#
newfilename = '{0}_SAMPLE_N_{1}.h5'.format(infilename.split('.h5')[0],nentries_to_grab)
df.to_hdf(newfilename, key='df', mode='w')
#

if DUMP_OPPOSITES:
    #newfilename = '{0}_SAMPLE_N_{1}_OPPOSITE.h5'.format(infilename.split('.h5')[0],len(df_alt))
    newfilename = '{0}_SAMPLE_N_{1}_OPPOSITE.h5'.format(infilename.split('.h5')[0],nvals-nentries_to_grab)
    df_alt.to_hdf(newfilename, key='df', mode='w')


