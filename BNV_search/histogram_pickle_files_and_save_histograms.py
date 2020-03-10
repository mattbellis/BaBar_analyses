import numpy as np
import matplotlib.pylab as plt

from babar_tools import display_histogram

import sys

import pickle

################################################################################

#OUTPUT_1235.pkl

ncuts = -1

infilenames = sys.argv[1:]
allvars = {}
histos = {}

for i,infile in enumerate(infilenames):
    print("Loading " + infile)
    x = pickle.load(open(infile,'rb'))

    if i==0:
        key = list(x.keys())[0]
        ncuts = len(x[key]['values'])

        for key in x.keys():
            allvars[key] = {}
            allvars[key]['values'] = list(x[key]['values'])
            allvars[key]['xlabel'] = x[key]['xlabel']
            allvars[key]['ylabel'] = x[key]['ylabel']
            allvars[key]['range'] = x[key]['range']

            histos[key] = {}
            histos[key]['h'] = []
            histos[key]['xlabel'] = x[key]['xlabel']
            histos[key]['ylabel'] = x[key]['ylabel']
            histos[key]['range'] = x[key]['range']
    else:
        for key in x.keys():
            vals_for_all_cuts = x[key]['values']
            for i,v in enumerate(vals_for_all_cuts):
                allvars[key]['values'][i] += v

#print(allvars)

for key in allvars.keys():
    var = allvars[key]
    bins = 100#allvars[key]['bins']
    r = allvars[key]['range']

    values = var['values']
    for vals in values:
        h = np.histogram(vals,bins=bins,range=r)
        histos[key]['h'].append(h)

print(histos)

plt.figure()
icount = 0
for key in histos.keys():
    plt.subplot(6,6,icount+1)
    print(key)
    hist = histos[key]
    xlabel = hist['xlabel']
    ylabel = hist['ylabel']
    histograms = hist['h']
    for h in histograms:
        display_histogram(h, xlabel, ylabel)

    icount += 1

print("Done caculating...")
plt.show()
