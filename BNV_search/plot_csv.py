import sys

import pandas as pd

import numpy as np
import matplotlib.pylab as plt

df = pd.read_csv(sys.argv[1])

names = df.columns.values

plt.figure()
for i,name in enumerate(names):
    plt.subplot(5,4,i+1)

    if name.find('cos')>=0:
        df[name].hist(bins=100,range=(-1,1),label=name)
    elif name.find('3')>=0:
        df[name].hist(bins=100,range=(2,3.0),label=name)
    else:
        df[name].hist(label=name, range=(0,1),bins=2)

    plt.legend()

#plt.tight_layout()

plt.show()
