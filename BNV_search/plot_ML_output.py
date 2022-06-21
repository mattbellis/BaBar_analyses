import numpy as np
import matplotlib.pylab as plt


import sys

infilename = sys.argv[1]


data = np.load(infilename)

print(len(data[(data>=0.2)&(data<=1.0)]))


# For unblinding
#plt.hist(data,bins=80, range=(0.2,1.0))
# Blinded
plt.hist(data,bins=60, range=(0.2,0.80))

plt.xlim(0.2, 1.0)

plt.xlabel('Tensorflow output')

name = 'tensorflow_output_variable_' + infilename.split('.')[0] + ".png"
plt.savefig('plots_nmu/' + name)

plt.show()

