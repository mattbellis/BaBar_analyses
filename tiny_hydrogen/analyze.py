import uproot
import awkward as ak
import numpy as np
import matplotlib.pylab as plt

import sys

infilenames = sys.argv[1:]

#'''
nfiles = len(infilenames)
data = {}
data['nMass'] = [[],[],[],[],[]]
data['eenergy'] = [[],[],[],[],[]]
data['penergy'] = [[],[],[],[],[]]

for i,infilename in enumerate(infilenames):
    name = infilename+":ntp1;1"
    print(i,nfiles,name)

    events = uproot.open(name)
    #print(events.keys())
    nevents = len(events['nn'].array())

    nn = events['nn'].array()
    nMass = events['nMass'].array()
    nd1Idx = events['nd1Idx'].array()
    nd2Idx = events['nd2Idx'].array()
    eenergy = events['eenergy'].array()
    penergy = events['penergy'].array()

    for j in range(nevents):
        #event = events[j]
        #print(event.keys())
        #print(len(nn),nevents)
        for n in range(nn[j]):
            idx1 = nd1Idx[j][n]
            idx2 = nd2Idx[j][n]

            data['nMass'][0].append(nMass[j][n])
            data['penergy'][0].append(penergy[j][idx1])
            data['eenergy'][0].append(eenergy[j][idx2])

            if eenergy[j][idx2]<0.200:
                data['nMass'][1].append(nMass[j][n])
                data['penergy'][1].append(penergy[j][idx1])
                data['eenergy'][1].append(eenergy[j][idx2])

            if eenergy[j][idx2]<0.100:
                data['nMass'][2].append(nMass[j][n])
                data['penergy'][2].append(penergy[j][idx1])
                data['eenergy'][2].append(eenergy[j][idx2])

            if eenergy[j][idx2]>0.060 and eenergy[j][idx2]<0.080:
                data['nMass'][3].append(nMass[j][n])
                data['penergy'][3].append(penergy[j][idx1])
                data['eenergy'][3].append(eenergy[j][idx2])

            if eenergy[j][idx2]>0.064 and eenergy[j][idx2]<0.070:
                data['nMass'][4].append(nMass[j][n])
                data['penergy'][4].append(penergy[j][idx1])
                data['eenergy'][4].append(eenergy[j][idx2])

            
        #print(nn)
        #print(nMass)
        #print(nd1Idx)
        #print(nd2Idx)
        #print(eenergy)
        #print(penergy)
        #exit()
    #print(events['nMass'])
    #masses += ak.to_numpy(ak.flatten(events['nMass'].array())).tolist()
    #e_energies += ak.to_numpy(ak.flatten(events['eenergy'].array())).tolist()
#'''



#print(masses)
ee_ranges = [(0,5),(0,0.3),(0,0.120), (0,0.120), (0,0.120)]
pe_ranges = [(0,5),(0,5),(0,5),(0,5),(0,5)]

for i in range(0,5):
    plt.figure(figsize=(12,6))

    plt.subplot(2,2,1)
    plt.hist(data['nMass'][i],range=(0.0,1.3),bins=100)
    plt.xlabel(r'$M_{pe^-}$ [GeV/c$^2$]',fontsize=18)

    plt.subplot(2,2,3)
    plt.hist(data['eenergy'][i],range=ee_ranges[i],bins=100)
    plt.xlabel(r'$E_{e^-}$ [GeV]',fontsize=18)

    plt.subplot(2,2,4)
    plt.hist(data['penergy'][i],range=pe_ranges[i],bins=100)
    plt.xlabel(r'$E_{p}$ [GeV]',fontsize=18)
    plt.tight_layout()

    name = f"plots/tiny_hydrogen_{i}.png"
    plt.savefig(name)


plt.show()


