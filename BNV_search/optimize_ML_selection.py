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

fom = sig_eps/((a/2.0) + np.sqrt(bkg_eps*B0))

plt.figure()
plt.subplot(2,2,1)
plt.plot(ml_output,fom)

plt.subplot(2,2,2)
plt.plot(bkg_eps,sig_eps)

plt.subplot(2,2,3)
plt.plot(ml_output,sig_eps)

plt.subplot(2,2,4)
plt.plot(ml_output,bkg_eps)

max_fom = max(fom)
idx = fom.to_list().index(max_fom)
print(max_fom,ml_output[idx],sig_eps[idx],bkg_eps[idx])

plt.show()


