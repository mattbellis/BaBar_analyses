import numpy as np
import matplotlib.pylab as plt

import ROOT

import sys

import zipfile

import myPIDselector
from myPIDselector import *

import lichen.lichen as lch

from babar_tools import vec_mag,angle,selectPID,invmass,recalc_energy,sph2cart
from babar_tools import particle_masses,particle_lunds
from babar_tools import eps,pps,pips,Kps,mups # The PID selectors for each particle

totx = []
toty = []
totz = []


allparts = [{}, {}, {}]

for pl in particle_lunds:
    allparts[0][pl] = []
    allparts[1][pl] = []
    allparts[2][pl] = []

# Uncomment this when running on the cluster or something
#plt.switch_backend('Agg')
################################################################################

#f = ROOT.TFile(sys.argv[1])
#f.ls()
#tree = f.Get("ntp1")

tree = ROOT.TChain("ntp1")
for infile in sys.argv[1:]:
    print(infile)
    tree.AddFile(infile)


nentries = tree.GetEntries()
#nentries = 1000

#outfilename = "%s.dat" % (sys.argv[1].split('/')[-1].split('.root')[0])
#outfilename = "%s.dat" % (sys.argv[1].split('.root')[0])
#outfile = open(outfilename,'w')

#outfilename = "proton_PID_sample_SP998.csv"
#outfilename_NOT = "NOT_proton_PID_sample_SP998.csv"
outfilename = "proton_PID_sample_SP9456.csv"
outfilename_NOT = "NOT_proton_PID_sample_SP9456.csv"
PIDtomatch = 2212
#outfilename = "mu_PID_sample.csv"
#outfilename_NOT = "NOT_mu_PID_sample.csv"
#PIDtomatch = 13
#outfilename = "electron_PID_sample.csv"
#outfilename_NOT = "NOT_electron_PID_sample.csv"
#PIDtomatch = 11

outfile = open(outfilename,'w')
outfile_NOT = open(outfilename_NOT,'w')


output = "cos(theta),"
output += "TightKMProton" + "," + "VeryTightKMProton" + "," + "SuperTightKMProton" + "," + \
      "TightBDTKaon" + "," + "VeryTightBDTKaon" + "," + "TightKMKaon" + "," + "VeryTightKMKaon" + "," + "SuperTightKMKaon" + "," + \
      "TightKMPion" + "," + "VeryTightKMPion" + "," + "SuperTightKMPion" + "," + \
      "TightKMElectron" + "," + "VeryTightKMElectron" + "," + "SuperTightKMElectron" + "," + \
      "BDTTightMuon" + "," + "BDTVeryTightMuon" + "," + "BDTTightMuonFakeRate" + "," + "BDTVeryTightMuonFakeRate" + "\n"
outfile.write(output)
outfile_NOT.write(output)

output = ""
output_NOT = ""
for i in range(nentries):

    if i%1000==0:
        print(i,nentries)

    if i>100000000:
        break

    tree.GetEntry(i)

    nvals = 0

    mcpid = []

    nmc = tree.mcLen
    #print("MC ----{0}----".format(nmc))
    for j in range(nmc):
        pid = abs(tree.mcLund[j])
        mcpid.append(pid)

    ntrks = tree.nTRK
    #print("----{0}----".format(ntrks))
    for j in range(ntrks):
        mcidx = tree.TRKMCIdx[j]
        p3 = tree.TRKp3[j]
        costh = tree.TRKcosth[j]
        lund = tree.TRKLund[j]
        #print("idx,len: ",idx,tree.mcLen, ntrks)
        #print("track", j)
        ebit,mubit,pibit,Kbit,pbit = tree.eSelectorsMap[j],tree.muSelectorsMap[j],tree.piSelectorsMap[j],tree.KSelectorsMap[j],tree.pSelectorsMap[j]
        #print(ebit,mubit,pibit,Kbit,pbit)
        eps.SetBits(ebit); mups.SetBits(mubit); pips.SetBits(pibit); Kps.SetBits(Kbit); pps.SetBits(pbit);

        isTightKMProton = int(pps.IsBitSet(15))
        isVeryTightKMProton = int(pps.IsBitSet(16))
        isSuperTightKMProton = int(pps.IsBitSet(17))

        isTightBDTKaon = int(Kps.IsBitSet(22))
        isVeryTightBDTKaon = int(Kps.IsBitSet(23))

        isTightKMKaon = int(Kps.IsBitSet(27))
        isVeryTightKMKaon = int(Kps.IsBitSet(28))
        isSuperTightKMKaon = int(Kps.IsBitSet(29))

        isTightKMPion = int(pips.IsBitSet(13))
        isVeryTightKMPion = int(pips.IsBitSet(14))
        isSuperTightKMPion = int(pips.IsBitSet(15))

        isTightKMElectron = int(eps.IsBitSet(9))
        isVeryTightKMElectron = int(eps.IsBitSet(10))
        isSuperTightKMElectron = int(eps.IsBitSet(11))

        isBDTTightMuon = int(mups.IsBitSet(18))
        isBDTVeryTightMuon = int(mups.IsBitSet(19))
        isBDTTightMuonFakeRate = int(mups.IsBitSet(22))
        isBDTVeryTightMuonFakeRate = int(mups.IsBitSet(23))


        if p3>2.0 and p3<2.6:
            '''
            print("---------------------------------")
            print(p3,costh,lund,mcidx,mcpid[mcidx])
            print("TightKMProton", "VeryTightKMProton", "SuperTightKMProton")
            print(isTightKMProton, isVeryTightKMProton, isSuperTightKMProton)
            print("TightBDTKaon", "VeryTightBDTKaon", "TightKMKaon", "VeryTightKMKaon", "SuperTightKMKaon")
            print(isTightBDTKaon, isVeryTightBDTKaon, isTightKMKaon, isVeryTightKMKaon, isSuperTightKMKaon)
            print("TightKMPion", "VeryTightKMPion", "SuperTightKMPion")
            print(isTightKMPion, isVeryTightKMPion, isSuperTightKMPion)
            print("TightKMElectron", "VeryTightKMElectron", "SuperTightKMElectron")
            print(isTightKMElectron, isVeryTightKMElectron, isSuperTightKMElectron)
            print("BDTTightMuon", "BDTVeryTightMuon", "BDTTightMuonFakeRate", "BDTVeryTightMuonFakeRate")
            print(isBDTTightMuon, isBDTVeryTightMuon, isBDTTightMuonFakeRate, isBDTVeryTightMuonFakeRate)
            '''

            if mcpid[mcidx]==PIDtomatch:
                output += "{0},".format(costh)
                output += "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17}\n".format(isTightKMProton, isVeryTightKMProton, isSuperTightKMProton,
                  isTightBDTKaon, isVeryTightBDTKaon, isTightKMKaon, isVeryTightKMKaon, isSuperTightKMKaon,
                  isTightKMPion, isVeryTightKMPion, isSuperTightKMPion,
                  isTightKMElectron, isVeryTightKMElectron, isSuperTightKMElectron,
                  isBDTTightMuon, isBDTVeryTightMuon, isBDTTightMuonFakeRate, isBDTVeryTightMuonFakeRate)
                break;

            else:
                output_NOT += "{0},".format(costh)
                output_NOT += "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17}\n".format(isTightKMProton, isVeryTightKMProton, isSuperTightKMProton,
                  isTightBDTKaon, isVeryTightBDTKaon, isTightKMKaon, isVeryTightKMKaon, isSuperTightKMKaon,
                  isTightKMPion, isVeryTightKMPion, isSuperTightKMPion,
                  isTightKMElectron, isVeryTightKMElectron, isSuperTightKMElectron,
                  isBDTTightMuon, isBDTVeryTightMuon, isBDTTightMuonFakeRate, isBDTVeryTightMuonFakeRate)


outfile.write(output)
outfile.close()

outfile_NOT.write(output_NOT)
outfile_NOT.close()
