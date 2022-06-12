import numpy as np
import matplotlib.pylab as plt


import sys

infilename = sys.argv[1]


data = np.load(infilename)


plt.hist(data,bins=200)


plt.show()

