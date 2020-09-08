import numpy as np
#import matplotlib.pylab as plt

import ROOT

import sys
import os

#import lichen.lichen as lch

from myPIDselector import *

import pickle
import pandas as pd

from babar_tools import vec_mag,angle,selectPID,invmass,recalc_energy,sph2cart
from babar_tools import particle_masses,particle_lunds
from babar_tools import eps,pps,pips,Kps,mups # The PID selectors for each particle

import argparse
parser = argparse.ArgumentParser(description='Process some files for B BNV search.')
parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
# decay can be pnu, ne, nmu
parser.add_argument('--decay', dest='decay', default="pnu", help='Decay to assume')
parser.add_argument('--dump-all-pid-flags', dest='dump_all_pid_flags', default=False, help='Dump all the PID flags to the output dict')
parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
args = parser.parse_args()

decay = args.decay


plotvars = {}
plotvars["nbnvbcand"] = {"values":[], "xlabel":r"# of BNV B-candidates", "ylabel":r"# E","range":(0,10)} 
plotvars["bnvbcandmass"] = {"values":[], "xlabel":r"Mass BNV B-candidate [GeV/c$^{2}$]", "ylabel":r"# E","range":(0,9)} 
plotvars["bnvbcandMES"] = {"values":[], "xlabel":r"BNV M$_{\rm ES}$ [GeV/c$^{2}$]", "ylabel":r"# E","range":(5.1,5.3)} 
plotvars["bnvbcandDeltaE"] = {"values":[], "xlabel":r"BNV $\Delta E$ [GeV]", "ylabel":r"# E","range":(-5,5)} 
plotvars["bnvprotp3"] = {"values":[], "xlabel":r"BNV proton $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,5)} 
plotvars["bnvlepp3"] = {"values":[], "xlabel":r"BNV lepton $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,5)} 

plotvars["tagbcandmass"] = {"values":[], "xlabel":r"Mass tag B-candidate [GeV/c$^{2}$]", "ylabel":r"# E","range":(0,9)} 
plotvars["tagbcandMES"] = {"values":[], "xlabel":r"tag M$_{\rm ES}$ [GeV/c$^{2}$]", "ylabel":r"# E","range":(5.1,5.3)} 
plotvars["tagbcandDeltaE"] = {"values":[], "xlabel":r"tag $\Delta E$ [GeV]", "ylabel":r"# E","range":(-5,5)} 
plotvars["tagq"] = {"values":[], "xlabel":r"tag charge", "ylabel":r"# E","range":(-5,5)} 
plotvars["missingmass"] = {"values":[], "xlabel":r"Missing mass [GeV/c$^2$]", "ylabel":r"# E","range":(-10,10)} 
plotvars["missingmom"] = {"values":[], "xlabel":r"Missing momentum [GeV/c]", "ylabel":r"# E","range":(0,10)} 
plotvars["missingE"] = {"values":[], "xlabel":r"Missing E [GeV]", "ylabel":r"# E","range":(-2,10)} 
plotvars["scalarmomsum"] = {"values":[], "xlabel":r"Scalar momentum sum [GeV/c]", "ylabel":r"# E","range":(0,15)} 
plotvars["nhighmom"] = {"values":[], "xlabel":r"# high p tracks", "ylabel":r"# E","range":(0,5)} 
plotvars["np"] = {"values":[], "xlabel":r"# proton", "ylabel":r"# E","range":(0,5)} 
plotvars["nmu"] = {"values":[], "xlabel":r"# muon", "ylabel":r"# E","range":(0,5)} 
plotvars["ne"] = {"values":[], "xlabel":r"# electron", "ylabel":r"# E","range":(0,5)} 
plotvars["pp"] = {"values":[], "xlabel":r"proton $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4)} 
plotvars["mup"] = {"values":[], "xlabel":r"muon $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4)} 
plotvars["ep"] = {"values":[], "xlabel":r"electron $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4)} 
plotvars["r2"] = {"values":[], "xlabel":r"R2", "ylabel":r"# E","range":(0,1)} 
plotvars["r2all"] = {"values":[], "xlabel":r"R2 all", "ylabel":r"# E","range":(0,1)} 
plotvars["thrustmag"] = {"values":[], "xlabel":r"Thrust mag", "ylabel":r"# E","range":(0,1)} 
plotvars["thrustmagall"] = {"values":[], "xlabel":r"Thrust mag all", "ylabel":r"# E","range":(0,1)} 
plotvars["thrustcosth"] = {"values":[], "xlabel":r"Thrust $\cos(\theta)$", "ylabel":r"# E","range":(-1,1)} 
plotvars["thrustcosthall"] = {"values":[], "xlabel":r"Thrust $\cos(\theta)$ all", "ylabel":r"# E","range":(-1,1)} 
plotvars["sphericityall"] = {"values":[], "xlabel":r"Sphericity all", "ylabel":r"# E","range":(0,1)} 
plotvars["ncharged"] = {"values":[], "xlabel":r"# charged particles", "ylabel":r"# E","range":(0,20)} 
plotvars["nphot"] = {"values":[], "xlabel":r"# photons","ylabel":r"# E","range":(0,20)} 
#plotvars["bnvprotIsTight"] = {"values":[], "xlabel":r"BNV proton IsTight", "ylabel":r"# E", "range":(-0.5, 1.5)}
#plotvars["bnvprotIsVeryTight"] = {"values":[], "xlabel":r"BNV proton IsVeryTight", "ylabel":r"# E", "range":(-0.5, 1.5)}
#plotvars["bnvprotIsSuperTight"] = {"values":[], "xlabel":r"BNV proton IsSuperTight", "ylabel":r"# E", "range":(-0.5, 1.5)}
#plotvars["bnvlepIsTight"] = {"values":[], "xlabel":r"BNV lepton IsTight", "ylabel":r"# E", "range":(-0.5, 1.5)}
#plotvars["bnvlepIsVeryTight"] = {"values":[], "xlabel":r"BNV lepton IsVeryTight", "ylabel":r"# E", "range":(-0.5, 1.5)}
#plotvars["bnvlepIsTightFakeRate"] = {"values":[], "xlabel":r"BNV lepton IsTightFakeRate", "ylabel":r"# E", "range":(-0.5, 1.5)}
#plotvars["bnvlepIsVeryTightFakeRate"] = {"values":[], "xlabel":r"BNV lepton IsVeryTightFakeRate", "ylabel":r"# E", "range":(-0.5, 1.5)}

# Make the plotvars for the PID flags
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

# Use this to write out only select cuts
plotvars_to_write_out = {}
for key in plotvars.keys():
    plotvars_to_write_out[key] = plotvars[key].copy()
    plotvars_to_write_out[key]['values'] = []

icuts_to_dump = [0,1,2,3,4]

cuts = []
#ncuts = 5
ncuts = 4 # Trying to dump to dataframe
for n in range(ncuts):
    #print(n)
    for key in plotvars.keys():
        plotvars[key]["values"].append([])

'''
#infilenames = sys.argv[1:]
lepton_to_study = sys.argv[1] # This should be ELECTRON OR MUON
topdir = sys.argv[2]
filestemp = os.listdir(topdir)

infilenames = []
for f in filestemp:
    if f.find('PID_skim.root')>=0:
        #files.append(f)
        infilenames.append(topdir+"/"+f)

print(len(infilenames))
print(infilenames[0])
#exit()
'''

tree = ROOT.TChain("analysis")
for i,infile in enumerate(args.infiles[0]):
    print(infile)
    tree.AddFile(infile)
    
    '''
    if i>100:
        break
    '''

nentries = tree.GetEntries()
print(nentries)
#exit()

invmasses = []
missmasses = []
nprotons = []
totqs = []

bcand = []
bcandMES = []
bcandDeltaE = []
bcandMM = []
tagbcand = []
tagbcandMES = []
tagbcandDeltaE = []
tagbcandMM = []

match_max = []
angles = []

nbcands = []

lep_p = []
prot_p = []

lepbits = [[], [], [], [], []]
protbits = [[], [], [], [], []]

ncharged = []
nphot = []

#filenames = sys.argv[1:]

################################################################################
def get_sptag(name):
    tag = None
    if name.find('AllEvents')>=0:
        # Data
        # basicPID_R24-AllEvents-Run1-OnPeak-R24-9_SKIMMED.root
        tag = 'AllEvents-' + name.split('AllEvents-')[1].split('-OnPeak-R24')[0] + '-OnPeak-R24'
    else:
        # MC
        tag = 'SP-{0}'.format(name.split('SP-')[1].split('-R24')[0])
    return tag
################################################################################

outfilename = None
outfilename_df = None
sptag = None

if args.outfile is None:
    sptag = get_sptag(args.infiles[0][0]) 
    #outfilename = 'OUTPUT_{0}_{1}_nfiles{2}.pkl'.format(decay,sptag,len(args.infiles[0]))
    #print(outfilename)
    #exit()

    # Better names?
    #fulldirName = '/data/physics/bellis/BaBar/rootfiles/cut_summary_files/{0}/{1}'.format(sptag,decay)
    #fulldirName = '{0}/{1}'.format(sptag,decay)

    fulldir_prepend = ''
    #fulldir_prepend = '/data/physics/bellis/BaBar/rootfiles/'
    fulldir_prepend = '/qnap/mbellis/bellis/BaBar/rootfiles/'

    fulldirNames = {}
    fulldirNames['pkl'] = '{2}/cut_summary_files_pickle/{0}/{1}'.format(sptag,decay,fulldir_prepend)
    fulldirNames['df'] =  '{2}/cut_summary_files_df/{0}/{1}'.format(sptag,decay,fulldir_prepend)

    for key in fulldirNames.keys():
        fulldirName = fulldirNames[key]
        try:
            # Create target Directory
            os.makedirs(fulldirName,exist_ok=True)
            print("Directory " , fulldirName ,  " Created ")
        except FileExistsError:
            print("Directory " , fulldirName ,  " already exists")

    #outfilename = filenames[0].split('/')[-1].split('.root')[0] + "_OUTPUT.root"
    #outfilename = sys.argv[1].split('.root')[0] + "_PID_skim.root"
    #outfilename = '/'.join(sys.argv[1].split('/')[:-1]) + "/" + dirName + "/" + sys.argv[1].split('/')[-1].split('.root')[0] + "_KINVARS_" + decay + ".root"
    filenumbers = []
    for f in args.infiles[0]:
        n = f.split('_SKIMMED_PID')[0].split('R24-')[-1]
        filenumbers.append(n)
    ntag = '-'.join(filenumbers)
    outfilename = '{0}/OUTPUT_{1}_nfiles{2}.pkl'.format(fulldirNames['pkl'],ntag,len(args.infiles[0]))
    outfilename_df = '{0}/OUTPUT_{1}_nfiles{2}.h5'.format(fulldirNames['df'],ntag,len(args.infiles[0]))
else:
    outfilename = '{0}.pkl'.format(args.outfile)
    outfilename_df = '{0}.df'.format(args.outfile)
print(outfilename)
print(outfilename_df)
    #exit()



for i in range(nentries):

    if i%10000==0:
        print(i,nentries)

    if i>100000000:
        break

    tree.GetEntry(i)

    nvals = 0

    r2 = tree.r2
    r2all = tree.r2all
    thrustmag = tree.thrustmag
    thrustmagall = tree.thrustmagall
    thrustcosth = tree.thrustcosth
    thrustcosthall = tree.thrustcosthall
    sphericityall = tree.sphericityall
        
    nphot = tree.ngamma
    ncharged = tree.npi + tree.nk + tree.nproton + tree.ne + tree.nmu

    nbnvbcand = tree.nbnvbcand
    bnvbcandmass = tree.bcand
    bnvbcandMES = tree.mes
    bnvbcandDeltaE = tree.dE
    bnvprotp3 = tree.bnvprotp3
    bnvlepp3 = tree.bnvlepp3

    tagbcandmass = tree.tagbcand
    tagbcandMES = tree.tagmes
    tagbcandDeltaE = tree.tagdE
    tagq = tree.tagq
    missingmass = tree.missingmass
    missingmom = tree.missingmom
    missingE = tree.missingE
    scalarmomsum = tree.scalarmomsum
    nhighmom = tree.nhighmom
    np = tree.nproton
    nmu = tree.nmu
    ne = tree.ne
    pq = tree.protonq
    muq = tree.muq
    eq = tree.eq
    pp = tree.protonp3
    mup = tree.mup3
    ep = tree.ep3


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

    # Should the low cut be 2.2 or 2.3? 
    cut1 = 1
    if decay=='pnu':
        #cut1 = np==1 and pp[0]>2.3 and pp[0]<2.8 
        cut1 = np>=1 and nhighmom==1 and nbnvbcand>=1 
        cut2 = ncharged>3
    elif decay=='nmu':
        #cut1 = nmu==1 and mup[0]>2.3 and mup[0]<2.8 
        cut1 = nmu>=1 and nhighmom==1 and nbnvbcand>=1
        cut2 = ncharged>3 
    elif decay=='ne':
        #cut1 = ne==1 and ep[0]>2.3 and ep[0]<2.8
        cut1 = ne>=1 and nhighmom==1 and nbnvbcand>=1
        cut2 = ncharged>3
    elif decay=='pmu' or decay=='pe':
        #cut1 = nbnvbcand==1 and bnvprotp3[0]>2.3 and bnvlepp3[0]>2.3 and bnvprotp3[0]<2.8 and bnvlepp3[0]<2.8
        cut1 = nbnvbcand>=1 and nhighmom==2
        #'''
        if decay=='pmu':
            #cut1 *= np==1 and nmu==1
            cut1 *= np>=1 and nmu>=1
        elif decay=='pe':
            #cut1 *= np==1 and ne==1
            cut1 *= np>=1 and ne>=1
        #'''
        cut2 = ncharged>5
        '''
        for inb in range(nbnvbcand):
            pidx = tree.bnvprotidx[inb]
            lepidx = tree.bnvlepidx[inb]
            print(pidx)
            print(protonIsTightKMProton[pidx], protonIsVeryTightKMProton[pidx], protonIsSuperTightKMProton[pidx])
            if decay=='pmu':
                print(lepidx)
                print(muIsBDTTightMuon[lepidx], muIsBDTVeryTightMuon[lepidx], muIsBDTTightMuonFakeRate[lepidx], muIsBDTVeryTightMuonFakeRate[lepidx])
        '''


    '''
    if decay=='pnu' or decay=='nmu' or decay=='ne':
        cut3 = nbnvbcand==1 
        #cut4 = missingmom>1 and missingE>1 # These cuts seem to be correlated with tagmass and tagdeltaE
    elif decay=='pmu' or decay=='pe':
        cut3 = nbnvbcand==1
        #cut4 = missingmom<2.6 and missingE<5 # These cuts seem to be correlated with tagmass and tagdeltaE
    '''

    # Make tighter momentum cuts for the last cut
    # For the signal selection
    lopcut = 2.3
    hipcut = 2.8

    # Maybe for sidebands in data
    if sptag.find('AllEvents')>=0:
        lopcut = 1.7
        hipcut = 10.0

    if decay=='pmu':
        cut3 = nbnvbcand==1 
        if nbnvbcand>0:
            cut3 *= bnvprotp3[0]>lopcut and bnvprotp3[0]<hipcut
            cut3 *= bnvlepp3[0]>lopcut and bnvlepp3[0]<hipcut
    elif decay=='pe':
        cut3 = nbnvbcand==1 
        if nbnvbcand>0:
            cut3 *= bnvprotp3[0]>lopcut and bnvprotp3[0]<hipcut
            cut3 *= bnvlepp3[0]>lopcut and bnvlepp3[0]<hipcut
    elif decay=='pnu':
        cut3 = nbnvbcand==1 
        if nbnvbcand>0:
            cut3 *= bnvprotp3[0]>lopcut and bnvprotp3[0]<hipcut
            cut3 *= bnvlepp3[0]>0.0 # This is missing momentum so we won't cut hard on it right now
    elif decay=='nmu':
        cut3 = nbnvbcand==1 
        if nbnvbcand>0:
            cut3 *= bnvprotp3[0]>0.0 # This is missing momentum so we won't cut hard on it right now
            cut3 *= bnvlepp3[0]>lopcut and bnvlepp3[0]<hipcut
    elif decay=='ne':
        cut3 = nbnvbcand==1 
        if nbnvbcand>0:
            cut3 *= bnvprotp3[0]>0.0 # This is missing momentum so we won't cut hard on it right now
            cut3 *= bnvlepp3[0]>lopcut and bnvlepp3[0]<hipcut

    cuts = [1, cut1, (cut2*cut1), (cut1*cut2*cut3)]#, (cut1*cut2*cut3*cut4)]#, (cut1*cut2*cut3*cut4*cut5), (cut1*cut2*cut3*cut4*cut5*cut6)]
    for icut,cut in enumerate(cuts):
        if cut:
            #print(icut)
            plotvars["r2"]["values"][icut].append(r2)
            plotvars["r2all"]["values"][icut].append(r2all)
            plotvars["thrustmag"]["values"][icut].append(thrustmag)
            plotvars["thrustmagall"]["values"][icut].append(thrustmagall)
            plotvars["thrustcosth"]["values"][icut].append(thrustcosth)
            plotvars["thrustcosthall"]["values"][icut].append(thrustcosthall)
            plotvars["sphericityall"]["values"][icut].append(sphericityall)

            plotvars["nphot"]["values"][icut].append(nphot)
            plotvars["ncharged"]["values"][icut].append(ncharged)

            plotvars["missingmom"]["values"][icut].append(missingmom)
            plotvars["missingE"]["values"][icut].append(missingE)
            plotvars["scalarmomsum"]["values"][icut].append(scalarmomsum)

            plotvars["nhighmom"]["values"][icut].append(nhighmom)

            plotvars["np"]["values"][icut].append(np)
            plotvars["nmu"]["values"][icut].append(nmu)
            plotvars["ne"]["values"][icut].append(ne)

            plotvars["nbnvbcand"]["values"][icut].append(nbnvbcand)

            for k in range(nbnvbcand):
                plotvars["bnvbcandmass"]["values"][icut].append(bnvbcandmass[k])
                plotvars["bnvbcandMES"]["values"][icut].append(bnvbcandMES[k])
                plotvars["bnvbcandDeltaE"]["values"][icut].append(bnvbcandDeltaE[k])
                plotvars["bnvprotp3"]["values"][icut].append(bnvprotp3[k])
                plotvars["bnvlepp3"]["values"][icut].append(bnvlepp3[k])

                plotvars["tagbcandmass"]["values"][icut].append(tagbcandmass[k])
                plotvars["tagbcandMES"]["values"][icut].append(tagbcandMES[k])
                plotvars["tagbcandDeltaE"]["values"][icut].append(tagbcandDeltaE[k])
                plotvars["tagq"]["values"][icut].append(tagq[k])
                plotvars["missingmass"]["values"][icut].append(missingmass[k])

                # Dump the PID flags for the BNV candidate decay products
                if not args.dump_all_pid_flags:
                    if decay=='pnu' or decay=='pmu' or decay=='pe':
                        pidx = tree.bnvprotidx[k]

                        plotvars["pp"]["values"][icut].append(pp[pidx])
                        plotvars["protonIsTightKMProton"]["values"][icut].append(protonIsTightKMProton[pidx])
                        plotvars["protonIsVeryTightKMProton"]["values"][icut].append(protonIsVeryTightKMProton[pidx])
                        plotvars["protonIsSuperTightKMProton"]["values"][icut].append(protonIsSuperTightKMProton[pidx])
                        plotvars["protonIsTightBDTKaon"]["values"][icut].append(protonIsTightBDTKaon[pidx])
                        plotvars["protonIsVeryTightBDTKaon"]["values"][icut].append(protonIsVeryTightBDTKaon[pidx])
                        plotvars["protonIsTightKMKaon"]["values"][icut].append(protonIsTightKMKaon[pidx])
                        plotvars["protonIsVeryTightKMKaon"]["values"][icut].append(protonIsVeryTightKMKaon[pidx])
                        plotvars["protonIsSuperTightKMKaon"]["values"][icut].append(protonIsSuperTightKMKaon[pidx])
                        plotvars["protonIsTightKMPion"]["values"][icut].append(protonIsTightKMPion[pidx])
                        plotvars["protonIsVeryTightKMPion"]["values"][icut].append(protonIsVeryTightKMPion[pidx])
                        plotvars["protonIsSuperTightKMPion"]["values"][icut].append(protonIsSuperTightKMPion[pidx])
                        plotvars["protonIsTightKMElectron"]["values"][icut].append(protonIsTightKMElectron[pidx])
                        plotvars["protonIsVeryTightKMElectron"]["values"][icut].append(protonIsVeryTightKMElectron[pidx])
                        plotvars["protonIsSuperTightKMElectron"]["values"][icut].append(protonIsSuperTightKMElectron[pidx])
                        plotvars["protonIsBDTTightMuon"]["values"][icut].append(protonIsBDTTightMuon[pidx])
                        plotvars["protonIsBDTVeryTightMuon"]["values"][icut].append(protonIsBDTVeryTightMuon[pidx])
                        plotvars["protonIsBDTTightMuonFakeRate"]["values"][icut].append(protonIsBDTTightMuonFakeRate[pidx])
                        plotvars["protonIsBDTVeryTightMuonFakeRate"]["values"][icut].append(protonIsBDTVeryTightMuonFakeRate[pidx])

                        #plotvars["bnvprotIsTight"]["values"][icut].append(protonIsTightKMProton[pidx])
                        #plotvars["bnvprotIsVeryTight"]["values"][icut].append(protonIsVeryTightKMProton[pidx])
                        #plotvars["bnvprotIsSuperTight"]["values"][icut].append(protonIsSuperTightKMProton[pidx])
                    elif decay=='nmu' or decay=='ne':
                        plotvars["pp"]["values"][icut].append(-999)
                        plotvars["protonIsTightKMProton"]["values"][icut].append(-999)
                        plotvars["protonIsVeryTightKMProton"]["values"][icut].append(-999)
                        plotvars["protonIsSuperTightKMProton"]["values"][icut].append(-999)
                        plotvars["protonIsTightBDTKaon"]["values"][icut].append(-999)
                        plotvars["protonIsVeryTightBDTKaon"]["values"][icut].append(-999)
                        plotvars["protonIsTightKMKaon"]["values"][icut].append(-999)
                        plotvars["protonIsVeryTightKMKaon"]["values"][icut].append(-999)
                        plotvars["protonIsSuperTightKMKaon"]["values"][icut].append(-999)
                        plotvars["protonIsTightKMPion"]["values"][icut].append(-999)
                        plotvars["protonIsVeryTightKMPion"]["values"][icut].append(-999)
                        plotvars["protonIsSuperTightKMPion"]["values"][icut].append(-999)
                        plotvars["protonIsTightKMElectron"]["values"][icut].append(-999)
                        plotvars["protonIsVeryTightKMElectron"]["values"][icut].append(-999)
                        plotvars["protonIsSuperTightKMElectron"]["values"][icut].append(-999)
                        plotvars["protonIsBDTTightMuon"]["values"][icut].append(-999)
                        plotvars["protonIsBDTVeryTightMuon"]["values"][icut].append(-999)
                        plotvars["protonIsBDTTightMuonFakeRate"]["values"][icut].append(-999)
                        plotvars["protonIsBDTVeryTightMuonFakeRate"]["values"][icut].append(-999)

                    if decay=='pmu' or decay=='nmu':
                        pidx = tree.bnvlepidx[k]

                        plotvars["mup"]["values"][icut].append(mup[pidx])
                        plotvars["muIsTightKMProton"]["values"][icut].append(muIsTightKMProton[pidx])
                        plotvars["muIsVeryTightKMProton"]["values"][icut].append(muIsVeryTightKMProton[pidx])
                        plotvars["muIsSuperTightKMProton"]["values"][icut].append(muIsSuperTightKMProton[pidx])
                        plotvars["muIsTightBDTKaon"]["values"][icut].append(muIsTightBDTKaon[pidx])
                        plotvars["muIsVeryTightBDTKaon"]["values"][icut].append(muIsVeryTightBDTKaon[pidx])
                        plotvars["muIsTightKMKaon"]["values"][icut].append(muIsTightKMKaon[pidx])
                        plotvars["muIsVeryTightKMKaon"]["values"][icut].append(muIsVeryTightKMKaon[pidx])
                        plotvars["muIsSuperTightKMKaon"]["values"][icut].append(muIsSuperTightKMKaon[pidx])
                        plotvars["muIsTightKMPion"]["values"][icut].append(muIsTightKMPion[pidx])
                        plotvars["muIsVeryTightKMPion"]["values"][icut].append(muIsVeryTightKMPion[pidx])
                        plotvars["muIsSuperTightKMPion"]["values"][icut].append(muIsSuperTightKMPion[pidx])
                        plotvars["muIsTightKMElectron"]["values"][icut].append(muIsTightKMElectron[pidx])
                        plotvars["muIsVeryTightKMElectron"]["values"][icut].append(muIsVeryTightKMElectron[pidx])
                        plotvars["muIsSuperTightKMElectron"]["values"][icut].append(muIsSuperTightKMElectron[pidx])
                        plotvars["muIsBDTTightMuon"]["values"][icut].append(muIsBDTTightMuon[pidx])
                        plotvars["muIsBDTVeryTightMuon"]["values"][icut].append(muIsBDTVeryTightMuon[pidx])
                        plotvars["muIsBDTTightMuonFakeRate"]["values"][icut].append(muIsBDTTightMuonFakeRate[pidx])
                        plotvars["muIsBDTVeryTightMuonFakeRate"]["values"][icut].append(muIsBDTVeryTightMuonFakeRate[pidx])

                    elif decay=='pe' or decay=='nnu' or decay=='ne':
                        plotvars["mup"]["values"][icut].append(-999)
                        plotvars["muIsTightKMProton"]["values"][icut].append(-999)
                        plotvars["muIsVeryTightKMProton"]["values"][icut].append(-999)
                        plotvars["muIsSuperTightKMProton"]["values"][icut].append(-999)
                        plotvars["muIsTightBDTKaon"]["values"][icut].append(-999)
                        plotvars["muIsVeryTightBDTKaon"]["values"][icut].append(-999)
                        plotvars["muIsTightKMKaon"]["values"][icut].append(-999)
                        plotvars["muIsVeryTightKMKaon"]["values"][icut].append(-999)
                        plotvars["muIsSuperTightKMKaon"]["values"][icut].append(-999)
                        plotvars["muIsTightKMPion"]["values"][icut].append(-999)
                        plotvars["muIsVeryTightKMPion"]["values"][icut].append(-999)
                        plotvars["muIsSuperTightKMPion"]["values"][icut].append(-999)
                        plotvars["muIsTightKMElectron"]["values"][icut].append(-999)
                        plotvars["muIsVeryTightKMElectron"]["values"][icut].append(-999)
                        plotvars["muIsSuperTightKMElectron"]["values"][icut].append(-999)
                        plotvars["muIsBDTTightMuon"]["values"][icut].append(-999)
                        plotvars["muIsBDTVeryTightMuon"]["values"][icut].append(-999)
                        plotvars["muIsBDTTightMuonFakeRate"]["values"][icut].append(-999)
                        plotvars["muIsBDTVeryTightMuonFakeRate"]["values"][icut].append(-999)

                    if decay=='pe' or decay=='ne':
                        pidx = tree.bnvlepidx[k]

                        plotvars["ep"]["values"][icut].append(ep[pidx])
                        plotvars["eIsTightKMProton"]["values"][icut].append(eIsTightKMProton[pidx])
                        plotvars["eIsVeryTightKMProton"]["values"][icut].append(eIsVeryTightKMProton[pidx])
                        plotvars["eIsSuperTightKMProton"]["values"][icut].append(eIsSuperTightKMProton[pidx])
                        plotvars["eIsTightBDTKaon"]["values"][icut].append(eIsTightBDTKaon[pidx])
                        plotvars["eIsVeryTightBDTKaon"]["values"][icut].append(eIsVeryTightBDTKaon[pidx])
                        plotvars["eIsTightKMKaon"]["values"][icut].append(eIsTightKMKaon[pidx])
                        plotvars["eIsVeryTightKMKaon"]["values"][icut].append(eIsVeryTightKMKaon[pidx])
                        plotvars["eIsSuperTightKMKaon"]["values"][icut].append(eIsSuperTightKMKaon[pidx])
                        plotvars["eIsTightKMPion"]["values"][icut].append(eIsTightKMPion[pidx])
                        plotvars["eIsVeryTightKMPion"]["values"][icut].append(eIsVeryTightKMPion[pidx])
                        plotvars["eIsSuperTightKMPion"]["values"][icut].append(eIsSuperTightKMPion[pidx])
                        plotvars["eIsTightKMElectron"]["values"][icut].append(eIsTightKMElectron[pidx])
                        plotvars["eIsVeryTightKMElectron"]["values"][icut].append(eIsVeryTightKMElectron[pidx])
                        plotvars["eIsSuperTightKMElectron"]["values"][icut].append(eIsSuperTightKMElectron[pidx])
                        plotvars["eIsBDTTightMuon"]["values"][icut].append(eIsBDTTightMuon[pidx])
                        plotvars["eIsBDTVeryTightMuon"]["values"][icut].append(eIsBDTVeryTightMuon[pidx])
                        plotvars["eIsBDTTightMuonFakeRate"]["values"][icut].append(eIsBDTTightMuonFakeRate[pidx])
                        plotvars["eIsBDTVeryTightMuonFakeRate"]["values"][icut].append(eIsBDTVeryTightMuonFakeRate[pidx])

                    elif decay=='pmu' or decay=='nnu' or decay=='nmu':
                        plotvars["ep"]["values"][icut].append(-999)
                        plotvars["eIsTightKMProton"]["values"][icut].append(-999)
                        plotvars["eIsVeryTightKMProton"]["values"][icut].append(-999)
                        plotvars["eIsSuperTightKMProton"]["values"][icut].append(-999)
                        plotvars["eIsTightBDTKaon"]["values"][icut].append(-999)
                        plotvars["eIsVeryTightBDTKaon"]["values"][icut].append(-999)
                        plotvars["eIsTightKMKaon"]["values"][icut].append(-999)
                        plotvars["eIsVeryTightKMKaon"]["values"][icut].append(-999)
                        plotvars["eIsSuperTightKMKaon"]["values"][icut].append(-999)
                        plotvars["eIsTightKMPion"]["values"][icut].append(-999)
                        plotvars["eIsVeryTightKMPion"]["values"][icut].append(-999)
                        plotvars["eIsSuperTightKMPion"]["values"][icut].append(-999)
                        plotvars["eIsTightKMElectron"]["values"][icut].append(-999)
                        plotvars["eIsVeryTightKMElectron"]["values"][icut].append(-999)
                        plotvars["eIsSuperTightKMElectron"]["values"][icut].append(-999)
                        plotvars["eIsBDTTightMuon"]["values"][icut].append(-999)
                        plotvars["eIsBDTVeryTightMuon"]["values"][icut].append(-999)
                        plotvars["eIsBDTTightMuonFakeRate"]["values"][icut].append(-999)
                        plotvars["eIsBDTVeryTightMuonFakeRate"]["values"][icut].append(-999)


                '''
                if decay=='nmu' or decay=='ne' or decay=='pmu' or decay=='pe':
                    lepidx = tree.bnvlepidx[k]
                    plotvars["bnvlepIsTight"]["values"][icut].append(muIsBDTTightMuon[lepidx])
                    plotvars["bnvlepIsVeryTight"]["values"][icut].append(muIsBDTVeryTightMuon[lepidx])
                    plotvars["bnvlepIsTightFakeRate"]["values"][icut].append(muIsBDTTightMuonFakeRate[lepidx])
                    plotvars["bnvlepIsVeryTightFakeRate"]["values"][icut].append(muIsBDTVeryTightMuonFakeRate[lepidx])
                elif decay=='pnu':
                    plotvars["bnvlepIsTight"]["values"][icut].append(-1)
                    plotvars["bnvlepIsVeryTight"]["values"][icut].append(-1)
                    plotvars["bnvlepIsTightFakeRate"]["values"][icut].append(-1)
                    plotvars["bnvlepIsVeryTightFakeRate"]["values"][icut].append(-1)
                '''

            if args.dump_all_pid_flags:
                for k in range(np):
                    plotvars["pp"]["values"][icut].append(pp[k])

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
                    plotvars["mup"]["values"][icut].append(mup[k])

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
                    plotvars["ep"]["values"][icut].append(ep[k])

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

    #nbcand += 1
        
    #totqs.append(totq)
    #nbcands.append(nbcand)

#exit()

################################################
# Write only specific cuts out to a file
################################################
for key in plotvars.keys():
    #print(key)
    a = plotvars[key]
    # Need to clear the values
    #plotvars_to_write_out[key]['values'] = []
    for i in range(len(a['values'])):
        if i in icuts_to_dump:
            plotvars_to_write_out[key]['values'].append(a['values'][i])

######################
# Write out to a file
######################
outfile = open(outfilename,'wb')
pickle.dump(plotvars_to_write_out,outfile)
outfile.close()

################################################
# Write to dataframe and write out the last cut
df_dict = {}
for key in plotvars.keys():
    # These may be of different length so we don't include them
    if decay=='pmu':
        if key.find('eIs')>=0 or key=='ep':
            continue
    elif decay=='pe':
        if key.find('muIs')>=0 or key=='mup':
            continue
    elif decay=='pnu':
        if key.find('eIs')>=0 or key.find('muIs')>=0 or key=='ep' or key=='mup':
            continue
    elif decay=='nmu':
        if key.find('protonIs')>=0 or key.find('eIs')>=0 or key=='ep' or key=='pp':
            continue
    elif decay=='ne':
        if key.find('protonIs')>=0 or key.find('muIs')>=0 or key=='pp' or key=='mup':
            continue

    df_dict[key] = plotvars[key]['values'][ncuts-1].copy()
    #print(key,len(df_dict[key]))

# Dump out some subset to a pandas dataframe
#print(df_dict.keys())
df = pd.DataFrame.from_dict(df_dict)
#print(df.columns)
df.to_hdf(outfilename_df,'df',mode='w')


################################################

print('Processed {0} files for {1}'.format(len(args.infiles),"1"))#,sptag))

#exit()

#print(bcand)
for icut,cut in enumerate(cuts):
    for j,key in enumerate(plotvars.keys()):
        var = plotvars[key]
        if j==0:
            print("cut {0}   # remaining {1}".format(icut,len(var["values"][icut])/nentries))
#exit()


'''
for icut,cut in enumerate(cuts):
    plt.figure(figsize=(10,6))
    for j,key in enumerate(plotvars.keys()):
        var = plotvars[key]
        plt.subplot(5,6,1+j)
        if key=="nphot" or key=="ncharged":
            lch.hist(var["values"][icut],range=var["range"],bins=20,alpha=0.2,markersize=0.5)
        else:
            lch.hist(var["values"][icut],range=var["range"],bins=50,alpha=0.2,markersize=0.5)
        plt.xlabel(var["xlabel"],fontsize=8)
        plt.ylabel(var["ylabel"],fontsize=8)
        if j==0:
            print("cut {0}   # remaining {1}".format(icut,len(var["values"][icut])))

    plt.tight_layout()

plt.show()
'''
