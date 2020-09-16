import matplotlib.pylab as plt
import  numpy as np
import pandas as pd
import sys

infilename = sys.argv[1]

df = pd.read_hdf(infilename)

sig_eps = df['tpr_keras']
bkg_eps = df['fpr_keras']

ml_output = df['thresholds_keras']

a = 4.0
B0 = 240.0
#B0 = 1000.0

fom = sig_eps/((a/2.0) + np.sqrt(bkg_eps*B0))

plt.figure(figsize=(12,6))
plt.subplot(2,2,1)
plt.plot(ml_output,fom)
plt.xlabel('ML output')
plt.ylabel('Punzi figure-of-merit')

plt.subplot(2,2,2)
plt.plot(bkg_eps,sig_eps)
plt.xlabel('Background efficiency')
plt.ylabel('Signal efficiency')

plt.subplot(2,2,3)
plt.plot(ml_output,sig_eps)
plt.xlabel('ML output')
plt.ylabel('Signal efficiency')

plt.subplot(2,2,4)
plt.plot(ml_output,bkg_eps)
plt.xlabel('ML output')
plt.ylabel('Background efficiency')

plt.tight_layout()

max_fom = max(fom)
idx = fom.to_list().index(max_fom)
print('Max figure of merit:   {0:2f}'.format(max_fom))
print('ML output for max fom: {0:2f}'.format(ml_output[idx]))
print('Sig eff for max fom:   {0:2f}'.format(sig_eps[idx]))
print('Bkj eff for max fom:   {0:2f}'.format(bkg_eps[idx]))

plt.show()


