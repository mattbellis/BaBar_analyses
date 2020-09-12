import pandas as pd
import sys

infilename = sys.argv[1]

nentries_to_grab = int(sys.argv[2])

df_org = pd.read_hdf(infilename)

print("Org entries: {0}".format(len(df_org)))

df = df_org.sample(n=nentries_to_grab)

newfilename = '{0}_SAMPLE_N_{1}.h5'.format(infilename.split('.h5')[0],nentries_to_grab)

df.to_hdf(newfilename, key='df', mode='w')


