import pandas as pd
import sys
import numpy as np

infilenames = sys.argv[1:]

print(infilenames)

for infilename in infilenames:

    print(infilename)

    df = pd.read_hdf(infilename)

    columns = list(df.columns)
    #print(columns)
    if 'missingmass_byhand' in columns:
        print('Already in there!')
        print('Exiting.....')
        continue

    E = df['missingE'].values
    p = df['missingmom'].values

    mm2 = E**2 - p**2

    mm = mm2.copy()
    mm[mm>=0] = np.sqrt(mm2[mm2>=0])
    mm[mm<0] = -np.sqrt(np.abs(mm2[mm2<0]))

    #print(mm)
    #print(mm2)

    df['missingmass_byhand'] = mm
    df['missingmass2_byhand'] = mm2


    df.to_hdf(infilename,'df',mode='a')

