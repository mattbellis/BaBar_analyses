import pandas as pd
import numpy as np

import sys

infilenames = sys.argv[1:]

columns = [[], []]

for i,infilename in enumerate(infilenames):
    df = pd.read_hdf(infilename)

    for col in df.columns:
        if col.find('Is')>=0:
            continue
        columns[i].append(col)
        print(col)
    print("===========")

common = []
different = []

for col in columns[0]:
    if col in columns[1]:
        #print(f"{col}\n{columns[1]}\n")
        common.append(col)
    else:
        print(f"{col}\n{columns[1]}\n")
        different.append(col)

for col in columns[1]:
    if col not in columns[0] and col not in different:
        different.append(col)

print("\ncommon: ----------")
for col in common:
    print(f"\t{col}")
print("\ndifferent: ----------")
for col in different:
    print(f"\t{col}")


print("\nEverything!!!!!!!!!!!!!")
for a,b in zip(np.sort(columns[0]),np.sort(columns[1])):

    print(a,b)
