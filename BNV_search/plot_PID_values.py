import numpy as np
import matplotlib.pylab as plt

import ROOT

import sys
import os

import lichen as lch


################################################################################
def get_sptag(name):
    tag = None
    if name.find('AllEvents')>=0:
        # Data
        # basicPID_R24-AllEvents-Run1-OnPeak-R24-9_SKIMMED.root
        tag = name.split('basicPID_R24-AllEvents-')[1].split('-OnPeak-R24-')[0]
    else:
        # MC
        tag = name.split('basicPID_R24-SP-')[1].split('-R24-')[0]
    return tag
################################################################################


# Make the plotvars for the PID flags
plotvars = {}

particles = ['proton','e','mu']
flags = ['IsTightKMProton',
         'IsVeryTightKMProton',
         'IsSuperTightKMProton',
         'IsTightBDTKaon',
         'IsVeryTightBDTKaon',
         'IsTightKMKaon',
         'IsVeryTightKMKaon',
         'IsSuperTightKMKaon',
         'IsTightKMPion',
         'IsVeryTightKMPion',
         'IsSuperTightKMPion',
         'IsTightKMElectron',
         'IsVeryTightKMElectron',
         'IsSuperTightKMElectron',
         'IsBDTTightMuon',
         'IsBDTVeryTightMuon',
         'IsBDTTightMuonFakeRate',
         'IsBDTVeryTightMuonFakeRate']

for particle in particles:
    for flag in flags:
        name = '{0}{1}'.format(particle,flag)
        plotvars[name] = {"values":[], "xlabel":name,"ylabel":r"#","range":(-2,2)}


ncuts = 1
for n in range(ncuts):
    for key in plotvars.keys():
        plotvars[key]["values"].append([])


infilenames = sys.argv[1:]

tree = ROOT.TChain("analysis")
for i,infile in enumerate(infilenames):
    print(infile)
    tree.AddFile(infile)

tree.Print()
nentries = tree.GetEntries()
print(nentries)
#exit()

for i in range(nentries):

    if i%1000==0:
        print(i,nentries)

    tree.GetEntry(i)

    nproton = tree.nproton
    nmu = tree.nmu
    ne = tree.ne

    protonIsTightKMProton = tree.protonIsTightKMProton
    protonIsVeryTightKMProton = tree.protonIsVeryTightKMProton
    protonIsSuperTightKMProton = tree.protonIsSuperTightKMProton
    protonIsTightBDTKaon = tree.protonIsTightBDTKaon
    protonIsVeryTightBDTKaon = tree.protonIsVeryTightBDTKaon
    protonIsTightKMKaon = tree.protonIsTightKMKaon
    protonIsVeryTightKMKaon = tree.protonIsVeryTightKMKaon
    protonIsSuperTightKMKaon = tree.protonIsSuperTightKMKaon
    protonIsTightKMPion = tree.protonIsTightKMPion
    protonIsVeryTightKMPion = tree.protonIsVeryTightKMPion
    protonIsSuperTightKMPion = tree.protonIsSuperTightKMPion
    protonIsTightKMElectron = tree.protonIsTightKMElectron
    protonIsVeryTightKMElectron = tree.protonIsVeryTightKMElectron
    protonIsSuperTightKMElectron = tree.protonIsSuperTightKMElectron
    protonIsBDTTightMuon = tree.protonIsBDTTightMuon
    protonIsBDTVeryTightMuon = tree.protonIsBDTVeryTightMuon
    protonIsBDTTightMuonFakeRate = tree.protonIsBDTTightMuonFakeRate
    protonIsBDTVeryTightMuonFakeRate = tree.protonIsBDTVeryTightMuonFakeRate

    muIsTightKMProton = tree.muIsTightKMProton
    muIsVeryTightKMProton = tree.muIsVeryTightKMProton
    muIsSuperTightKMProton = tree.muIsSuperTightKMProton
    muIsTightBDTKaon = tree.muIsTightBDTKaon
    muIsVeryTightBDTKaon = tree.muIsVeryTightBDTKaon
    muIsTightKMKaon = tree.muIsTightKMKaon
    muIsVeryTightKMKaon = tree.muIsVeryTightKMKaon
    muIsSuperTightKMKaon = tree.muIsSuperTightKMKaon
    muIsTightKMPion = tree.muIsTightKMPion
    muIsVeryTightKMPion = tree.muIsVeryTightKMPion
    muIsSuperTightKMPion = tree.muIsSuperTightKMPion
    muIsTightKMElectron = tree.muIsTightKMElectron
    muIsVeryTightKMElectron = tree.muIsVeryTightKMElectron
    muIsSuperTightKMElectron = tree.muIsSuperTightKMElectron
    muIsBDTTightMuon = tree.muIsBDTTightMuon
    muIsBDTVeryTightMuon = tree.muIsBDTVeryTightMuon
    muIsBDTTightMuonFakeRate = tree.muIsBDTTightMuonFakeRate
    muIsBDTVeryTightMuonFakeRate = tree.muIsBDTVeryTightMuonFakeRate

    eIsTightKMProton = tree.eIsTightKMProton
    eIsVeryTightKMProton = tree.eIsVeryTightKMProton
    eIsSuperTightKMProton = tree.eIsSuperTightKMProton
    eIsTightBDTKaon = tree.eIsTightBDTKaon
    eIsVeryTightBDTKaon = tree.eIsVeryTightBDTKaon
    eIsTightKMKaon = tree.eIsTightKMKaon
    eIsVeryTightKMKaon = tree.eIsVeryTightKMKaon
    eIsSuperTightKMKaon = tree.eIsSuperTightKMKaon
    eIsTightKMPion = tree.eIsTightKMPion
    eIsVeryTightKMPion = tree.eIsVeryTightKMPion
    eIsSuperTightKMPion = tree.eIsSuperTightKMPion
    eIsTightKMElectron = tree.eIsTightKMElectron
    eIsVeryTightKMElectron = tree.eIsVeryTightKMElectron
    eIsSuperTightKMElectron = tree.eIsSuperTightKMElectron
    eIsBDTTightMuon = tree.eIsBDTTightMuon
    eIsBDTVeryTightMuon = tree.eIsBDTVeryTightMuon
    eIsBDTTightMuonFakeRate = tree.eIsBDTTightMuonFakeRate
    eIsBDTVeryTightMuonFakeRate = tree.eIsBDTVeryTightMuonFakeRate

    icut = 0
    for k in range(nproton):
        plotvars["protonIsTightKMProton"]["values"][icut].append(protonIsTightKMProton[k])
        plotvars["protonIsVeryTightKMProton"]["values"][icut].append(protonIsVeryTightKMProton[k])
        plotvars["protonIsSuperTightKMProton"]["values"][icut].append(protonIsSuperTightKMProton[k])
        plotvars["protonIsTightBDTKaon"]["values"][icut].append(protonIsTightBDTKaon[k])
        plotvars["protonIsVeryTightBDTKaon"]["values"][icut].append(protonIsVeryTightBDTKaon[k])
        plotvars["protonIsTightKMKaon"]["values"][icut].append(protonIsTightKMKaon[k])
        plotvars["protonIsVeryTightKMKaon"]["values"][icut].append(protonIsVeryTightKMKaon[k])
        plotvars["protonIsSuperTightKMKaon"]["values"][icut].append(protonIsSuperTightKMKaon[k])
        plotvars["protonIsTightKMPion"]["values"][icut].append(protonIsTightKMPion[k])
        plotvars["protonIsVeryTightKMPion"]["values"][icut].append(protonIsVeryTightKMPion[k])
        plotvars["protonIsSuperTightKMPion"]["values"][icut].append(protonIsSuperTightKMPion[k])
        plotvars["protonIsTightKMElectron"]["values"][icut].append(protonIsTightKMElectron[k])
        plotvars["protonIsVeryTightKMElectron"]["values"][icut].append(protonIsVeryTightKMElectron[k])
        plotvars["protonIsSuperTightKMElectron"]["values"][icut].append(protonIsSuperTightKMElectron[k])
        plotvars["protonIsBDTTightMuon"]["values"][icut].append(protonIsBDTTightMuon[k])
        plotvars["protonIsBDTVeryTightMuon"]["values"][icut].append(protonIsBDTVeryTightMuon[k])
        plotvars["protonIsBDTTightMuonFakeRate"]["values"][icut].append(protonIsBDTTightMuonFakeRate[k])
        plotvars["protonIsBDTVeryTightMuonFakeRate"]["values"][icut].append(protonIsBDTVeryTightMuonFakeRate[k])

    for k in range(nmu):
        plotvars["muIsTightKMProton"]["values"][icut].append(muIsTightKMProton[k])
        plotvars["muIsVeryTightKMProton"]["values"][icut].append(muIsVeryTightKMProton[k])
        plotvars["muIsSuperTightKMProton"]["values"][icut].append(muIsSuperTightKMProton[k])
        plotvars["muIsTightBDTKaon"]["values"][icut].append(muIsTightBDTKaon[k])
        plotvars["muIsVeryTightBDTKaon"]["values"][icut].append(muIsVeryTightBDTKaon[k])
        plotvars["muIsTightKMKaon"]["values"][icut].append(muIsTightKMKaon[k])
        plotvars["muIsVeryTightKMKaon"]["values"][icut].append(muIsVeryTightKMKaon[k])
        plotvars["muIsSuperTightKMKaon"]["values"][icut].append(muIsSuperTightKMKaon[k])
        plotvars["muIsTightKMPion"]["values"][icut].append(muIsTightKMPion[k])
        plotvars["muIsVeryTightKMPion"]["values"][icut].append(muIsVeryTightKMPion[k])
        plotvars["muIsSuperTightKMPion"]["values"][icut].append(muIsSuperTightKMPion[k])
        plotvars["muIsTightKMElectron"]["values"][icut].append(muIsTightKMElectron[k])
        plotvars["muIsVeryTightKMElectron"]["values"][icut].append(muIsVeryTightKMElectron[k])
        plotvars["muIsSuperTightKMElectron"]["values"][icut].append(muIsSuperTightKMElectron[k])
        plotvars["muIsBDTTightMuon"]["values"][icut].append(muIsBDTTightMuon[k])
        plotvars["muIsBDTVeryTightMuon"]["values"][icut].append(muIsBDTVeryTightMuon[k])
        plotvars["muIsBDTTightMuonFakeRate"]["values"][icut].append(muIsBDTTightMuonFakeRate[k])
        plotvars["muIsBDTVeryTightMuonFakeRate"]["values"][icut].append(muIsBDTVeryTightMuonFakeRate[k])



    for k in range(ne):
        plotvars["eIsTightKMProton"]["values"][icut].append(eIsTightKMProton[k])
        plotvars["eIsVeryTightKMProton"]["values"][icut].append(eIsVeryTightKMProton[k])
        plotvars["eIsSuperTightKMProton"]["values"][icut].append(eIsSuperTightKMProton[k])
        plotvars["eIsTightBDTKaon"]["values"][icut].append(eIsTightBDTKaon[k])
        plotvars["eIsVeryTightBDTKaon"]["values"][icut].append(eIsVeryTightBDTKaon[k])
        plotvars["eIsTightKMKaon"]["values"][icut].append(eIsTightKMKaon[k])
        plotvars["eIsVeryTightKMKaon"]["values"][icut].append(eIsVeryTightKMKaon[k])
        plotvars["eIsSuperTightKMKaon"]["values"][icut].append(eIsSuperTightKMKaon[k])
        plotvars["eIsTightKMPion"]["values"][icut].append(eIsTightKMPion[k])
        plotvars["eIsVeryTightKMPion"]["values"][icut].append(eIsVeryTightKMPion[k])
        plotvars["eIsSuperTightKMPion"]["values"][icut].append(eIsSuperTightKMPion[k])
        plotvars["eIsTightKMElectron"]["values"][icut].append(eIsTightKMElectron[k])
        plotvars["eIsVeryTightKMElectron"]["values"][icut].append(eIsVeryTightKMElectron[k])
        plotvars["eIsSuperTightKMElectron"]["values"][icut].append(eIsSuperTightKMElectron[k])
        plotvars["eIsBDTTightMuon"]["values"][icut].append(eIsBDTTightMuon[k])
        plotvars["eIsBDTVeryTightMuon"]["values"][icut].append(eIsBDTVeryTightMuon[k])
        plotvars["eIsBDTTightMuonFakeRate"]["values"][icut].append(eIsBDTTightMuonFakeRate[k])
        plotvars["eIsBDTVeryTightMuonFakeRate"]["values"][icut].append(eIsBDTVeryTightMuonFakeRate[k])


plt.figure(figsize=(15,8))
icount = 0
tempkeys = list(plotvars.keys())
keys = []
for key in tempkeys:
    if key.find('protonIs')>=0:
        keys.append(key)
nkeys = len(keys)
#nkeys = 6
#exit()
for i in range(nkeys):
    for j in range(nkeys):
        ax = plt.subplot(nkeys,nkeys,i*nkeys + j +1)
        x = plotvars[keys[j]]['values'][0]
        y = plotvars[keys[i]]['values'][0]
        lch.hist2d(x,y,xbins=2,ybins=2,xrange=(0,2),yrange=(0,2),axes=ax)
        plt.gca().set_xlabel(keys[j],fontsize=6,rotation=45)
        plt.gca().set_ylabel(keys[i],fontsize=6,rotation=0)
        print(i*nkeys + j +1, keys[i], keys[j])
        
        icount += 1
#plt.tight_layout()

plt.show()


