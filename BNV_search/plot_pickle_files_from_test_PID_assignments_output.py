import numpy as np
import matplotlib.pylab as plt

import sys

import lichen.lichen as lch
import pickle

################################################################################

#OUTPUT_1235.pkl

infilenames = sys.argv[1:]
allplotvars = {}
for infile in infilenames:
    print("Loading " + infile)
    x = pickle.load(open(infile,'rb'))
    sptag = infile.split('OUTPUT_')[1].split('.pkl')[0]
    allplotvars[sptag] = x

print()
ncuts = 4
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

for j in range(nvars):
    if j>30:
        break

    width = 3*ncuts
    height = 0.5*nvars
    plt.figure(figsize=(width,height))

    varname = varnames[j]
    print(varname)

    for i,apvkey in enumerate(apvkeys):
        plotvars = allplotvars[apvkey]

        for icut in range(ncuts):

            plotindex = 1 + icut +  (i*ncuts)
            plt.subplot(nsp,ncuts,plotindex)

            var = plotvars[varname]

            if varname=="nphot" or varname=="ncharged":
                lch.hist_err(var["values"][icut],range=var["range"],bins=20,alpha=0.2,markersize=0.5,label=apvkey)
            else:
                lch.hist_err(var["values"][icut],range=var["range"],bins=50,alpha=0.2,markersize=0.5,label=apvkey)
            plt.xlabel(var["xlabel"],fontsize=12)
            plt.ylabel(var["ylabel"],fontsize=12)
            #print(len(var["values"][icut]))

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
            if icut==0:
                plt.legend()

    #plt.tight_layout()
plt.show()

exit()

for a in range(4):
    for icut,cut in enumerate(cuts):
        plt.figure(figsize=(10,6))
        for j,key in enumerate(plotvars.keys()):
            var = plotvars[key]
            plt.subplot(4,4,1+j)
            if key=="nphot" or key=="ncharged":
                lch.hist_err(var["values"][icut],range=var["range"],bins=20,alpha=0.2,markersize=0.5)
            else:
                lch.hist_err(var["values"][icut],range=var["range"],bins=50,alpha=0.2,markersize=0.5)
            plt.xlabel(var["xlabel"],fontsize=12)
            plt.ylabel(var["ylabel"],fontsize=12)
            print(len(var["values"][icut]))

        if icut==len(cuts)-1:
            plt.figure(figsize=(10,6))
            plt.subplot(1,1,1)
            plt.plot(plotvars["bcandMES"]["values"][icut],plotvars["bcandDeltaE"]["values"][icut],'.',alpha=0.8,markersize=2.0)
            plt.xlabel(plotvars["bcandMES"]["xlabel"],fontsize=12)
            plt.ylabel(plotvars["bcandMES"]["ylabel"],fontsize=12)
            plt.xlim(5.2,5.3)
            plt.ylim(-0.4,0.1)


            plt.tight_layout()
        plt.tight_layout()

plt.show()
