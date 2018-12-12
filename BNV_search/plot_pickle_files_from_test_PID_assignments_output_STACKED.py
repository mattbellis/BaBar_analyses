import numpy as np
import matplotlib.pylab as plt

import sys

import lichen.lichen as lch
import pickle

from raw_event_numbers_and_cross_section import *

ren = raw_event_numbers

scale_factors = {}
for key in ren["data"].keys():

    bkg = [1235, 1237, 1005, 998, 3429, 3981, 2400]
    for sp in bkg:
        key = "{0}".format(sp)
        xsec = ren["MC"][key]["xsec"]
        raw = ren["MC"][key]["raw"]
        sf = (raw/1e6)/(xsec*intlumi)
        scale_factors[key] = 1.0/sf


print(scale_factors)
#import seaborn as sns
#sns.set()

################################################################################

tag = "ELECTRON"
#tag = "MUON"

infilenames = ['OUTPUT_1235.pkl',
               'OUTPUT_1237.pkl',
               'OUTPUT_1005.pkl',
               'OUTPUT_998.pkl',
               'OUTPUT_3429.pkl',
               'OUTPUT_3981.pkl',
               #'OUTPUT_2400.pkl',
               ]
if tag=='ELECTRON':
    infilenames.append('OUTPUT_9457.pkl')
elif tag=='MUON':
    infilenames.append('OUTPUT_9456.pkl')

for i,infilename in enumerate(infilenames):
    infilenames[i] = infilename.replace('_','_{0}_'.format(tag))
print(infilenames)
#exit()

spnumbers = [name.split('_')[-1].split('.')[0] for name in infilenames]
labels = [r'$B^+B^-$',
          r'$B^0\bar{B}^0$',
          r'$c\bar{c}$',
          r'$u\bar{u},d\bar{d},s\bar{s}$',
          r'$\tau^+\tau^-$',
          r'$\mu^+\mu^-$',
          #r'$e^+e^-$',
          r'$B\rightarrow p e^-$']



#infilenames = sys.argv[1:]
allplotvars = {}
for infile in infilenames:
    print("Loading " + infile)
    x = pickle.load(open(infile,'rb'))
    sptag = infile.split('_')[-1].split('.pkl')[0]
    allplotvars[sptag] = x

#print(allplotvars)
print()
ncuts = 5
for apvkey in allplotvars.keys():
    plotvars = allplotvars[apvkey]
    #for icut,cut in enumerate(cuts):
    #print(plotvars.keys())
    nentries = len(plotvars['r2']['values'][0])
    output = "{0:4}   ".format(apvkey)
    for icut in range(ncuts):
        for j,key in enumerate([list(plotvars.keys())[0]]):
            var = plotvars[key]
            output += "{0:5.4f}   ".format(len(var["values"][icut])/nentries)

    print(output)
print()
#exit()


nsp = len(infilenames)
apvkeys = list(allplotvars.keys())
varnames = list(allplotvars[apvkeys[0]].keys())
nvars = len(varnames)

print(nsp,ncuts)

# Variables to plot
vtp = ['bcandMES', 'bcandDeltaE']

for varname in vtp:

    width = 4*ncuts
    height = 4
    #plt.figure(figsize=(width,height))

    for icut in range(ncuts):
        plt.figure(figsize=(6,4))

        plot_data = []
        weights = []

        sig_data = None

        for i,apvkey in enumerate(apvkeys):
            plotvars = allplotvars[apvkey]
            plotvars["bcandDeltaE"]["range"] = (-0.5,0.5)
            var = plotvars[varname]
            if apvkey!='9457' and apvkey!='9456': 

                data = var["values"][icut]
                plot_data.append(data)

                wt = scale_factors[apvkey]
                weights.append(wt*np.ones(len(data)))
            else:
                #plotvars["bcandDeltaE"]["range"] = (-0.5,0.5)
                #plotvars = allplotvars[apvkey]
                #var = plotvars[varname]
                data = var["values"][icut]
                sig_data = data

        plotindex = 1 + icut 
        #plt.subplot(1,ncuts,plotindex)
        plt.subplot(1,1,1)

        plt.hist(plot_data,range=var["range"],bins=50,alpha=1.0,weights=weights,label=labels,stacked=True)
        #print(sig_data[0:10])
        tot = 0
        for entry in plot_data:
            tot += len(entry)
        #wt = 0.01*(tot/len(sig_data))*np.ones(len(sig_data))
        wt = 0.001**np.ones(len(sig_data))
        plt.hist(sig_data,range=var["range"],bins=50,weights=wt,fill=False,label=labels[-1],color='k',histtype='step',linewidth=2)

        plt.xlabel(var["xlabel"],fontsize=12)
        plt.ylabel(var["ylabel"],fontsize=12)

        '''
        if icut==len(cuts)-1:
            plt.figure(figsize=(10,6))
            plt.subplot(1,1,1)
            plt.plot(plotvars["bcandMES"]["values"][icut],plotvars["bcandDeltaE"]["values"][icut],'.',alpha=0.8,markersize=2.0)
            plt.xlabel(plotvars["bcandMES"]["xlabel"],fontsize=12)
            plt.ylabel(plotvars["bcandMES"]["ylabel"],fontsize=12)
            plt.xlim(5.2,5.3)
            plt.ylim(-0.4,0.1)
        '''
        #if icut==0:
        if 1:
            plt.legend()

        plt.tight_layout()
        name = "plots/{0}_{1}_{2}.png".format(tag,varname,icut)
        plt.savefig(name)

    plt.tight_layout()
plt.show()

