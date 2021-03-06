import sys

import pandas as pd

import numpy as np
import matplotlib.pylab as plt

df = pd.read_hdf(sys.argv[1])

names = df.columns.values

for i,name in enumerate(names):

    if i%25==0:
        plt.figure()

    plt.subplot(5,5,i%25+1)

    if name.find('cos')>=0:
        df[name].hist(bins=100,range=(-1,1),label=name)
    elif name.find('3')>=0:
        df[name].hist(bins=100,range=(0,10.0),label=name)
    elif name.find('Is')>=0:
        df[name].hist(bins=2,range=(0,1),label=name)
    else:
        df[name].hist(label=name,bins=100)

    plt.legend()


#plt.tight_layout()

plt.show()
