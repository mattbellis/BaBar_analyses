import numpy as np
import matplotlib.pylab as plt

import babar_tools as bt

import sys

import pickle

################################################################################

#OUTPUT_1235.pkl

ncuts = -1

infilenames = sys.argv[1:]
#allvars = {}
#histos = {}

################################################################################
# Read in the files and combine all the data dictionaries
################################################################################
allvars,histos = bt.read_in_files_and_combine_all_the_dictionaries(infilenames)

#print(allvars)
################################################################################
# Make histograms with numpy and make a new set of dictionaries with this 
# information.
################################################################################
for key in allvars.keys():
    var = allvars[key]
    bins = 100#allvars[key]['bins']
    r = allvars[key]['range']
    print(key)
    if key.find('bnvbcandmass')>=0:
        r = (5.1,6.0)
    elif key.find('tagbcandmass')>=0:
        r = (2.0,8.0)
    elif key.find('bnvbcandMES')>=0:
        r = (5.2,5.3)
    elif key.find('tagbcandMES')>=0:
        r = (5.1,5.3)
    elif key.find('bnvbcandDeltaE')>=0:
        r = (-0.5,0.5)

    values = var['values']
    for vals in values:
        h = np.histogram(vals,bins=bins,range=r)
        histos[key]['h'].append(h)

print(histos)

################################################################################
# Display the histograms
################################################################################
plt.figure(figsize=(15,8))
icount = 0
print(list(histos.keys()))
#exit()
for key in histos.keys():
    plt.subplot(5,6,icount+1)
    print(key)
    hist = histos[key]
    xlabel = hist['xlabel']
    #ylabel = hist['ylabel']
    ylabel = r'# of entries'
    histograms = hist['h']
    for h in histograms:
        bt.display_histogram(h, xlabel, ylabel,xfontsize=8,yfontsize=8)

    icount += 1
plt.tight_layout()

print("Done caculating...")

################################################################################
# Display some
################################################################################
#kinvars_to_display = ['nbnvbcand', 'bnvbcandmass', 'bnvbcandMES', 'bnvbcandDeltaE', 'bnvprotp3', 'bnvlepp3', 'tagbcandmass', 'tagbcandMES', 'tagbcandDeltaE', 'tagq', 'missingmass', 'missingmom', 'missingE', 'scalarmomsum', 'nhighmom', 'np', 'nmu', 'ne', 'pp', 'mup', 'ep', 'r2', 'r2all', 'thrustmag', 'thrustmagall', 'thrustcosth', 'thrustcosthall', 'sphericityall', 'ncharged', 'nphot']
#'''
#kinvars_to_display = ['bnvbcandMES', 'bnvbcandDeltaE', 'tagbcandMES', 'tagbcandDeltaE', 'bnvprotp3', 'bnvlepp3', 'missingmass', 'missingmom', 'missingE', 'scalarmomsum']
kinvars_to_display = ['bnvbcandMES', 'bnvbcandDeltaE', 'tagbcandMES', 'tagbcandDeltaE', 'missingmass', 'missingmom', 'missingE', 'scalarmomsum']
plt.figure(figsize=(12,4))
icount = 0
print(list(histos.keys()))
#exit()
for key in kinvars_to_display:
    plt.subplot(2,4,icount+1)
    print(key)
    hist = histos[key]
    xlabel = hist['xlabel']
    #ylabel = hist['ylabel']
    ylabel = r'# of entries'
    histograms = hist['h']
    for h in histograms:
        bt.display_histogram(h, xlabel, ylabel)

    icount += 1
plt.tight_layout()

n = infilenames[0]
outfilename = "fig_{0}.png".format(n.split('/')[-1].split('.')[0])
print(outfilename)
plt.savefig(outfilename)
#'''

plt.show()
