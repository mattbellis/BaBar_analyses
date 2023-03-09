import numpy as np
import matplotlib.pylab as plt
import plotting_tools as pt

import sys
import os

infilename = sys.argv[1]
print(f"Processing file...{infilename}")
tag,label,decay = pt.get_sptag(infilename)
# Decay probably is something like _ne_ so remove the underscores
if decay is not None:
    decay = decay[1:-1]
print(tag,label,decay)
#exit()


data = np.load(infilename)
print(data)

lo = 0.2
hi = 1.0

print(f"nentries:                     {len(data)}")
print(f"nentries between {lo:3.1f} and {hi:3.1f}: {len(data[(data>=lo)&(data<=hi)])}")
print(f"full dataset between {lo:3.1f} and {hi:3.1f}: {20*len(data[(data>=lo)&(data<=hi)])}")


# For unblinding
plt.hist(data,bins=100, range=(5.2,5.3))
# Blinded
if infilename == 'PREDICTIONS_MES_Run_1_pmu.npy':
    plt.hist(data,bins=60, range=(5.2,5.266))
    print("Displaying only blinded region")

#plt.xlim(0.0, 1.0)

plt.xlabel(r'M$_{ES}$ (GeV/c$^2$)')

outdir = f'plots_{decay}'
if not os.path.exists(outdir):
   os.makedirs(outdir)

name = 'mes_delta_e_variable_' + infilename.split('.')[0] + ".png"
#plt.savefig('plots_nmu/' + name)
plt.savefig(f'{outdir}/{name}')

plt.show()

