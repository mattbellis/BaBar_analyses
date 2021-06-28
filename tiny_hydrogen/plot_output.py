import numpy as np
import matplotlib.pylab as plt

import sys

#infilenames = sys.argv[1:]

masses0 = np.loadtxt('ep_masses_pn.dat')
masses1 = np.loadtxt('ep_masses_nn.dat')
masses2 = np.loadtxt('ep_masses_pp.dat')

r = (0,11)
bins = 2000

plt.figure()
plt.subplot(3,1,1)
plt.hist(masses0,bins=bins,range=r)

plt.subplot(3,1,2)
plt.hist(masses1,bins=bins,range=r)

plt.subplot(3,1,3)
plt.hist(masses2,bins=bins,range=r)

plt.show()
