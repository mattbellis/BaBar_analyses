import numpy as np
#import matplotlib.pylab as plt

import ROOT

import sys
import os

#import lichen.lichen as lch

from myPIDselector import *

import pickle

from babar_tools import vec_mag,angle,selectPID,invmass,recalc_energy,sph2cart
from babar_tools import particle_masses,particle_lunds
from babar_tools import eps,pps,pips,Kps,mups # The PID selectors for each particle

import argparse
parser = argparse.ArgumentParser(description='Process some files for B BNV search.')
parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
# decay can be pnu, ne, nmu
parser.add_argument('--decay', dest='decay', default="pnu", help='Decay to assume')
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

# Use this to write out only select cuts
plotvars_to_write_out = {}
for key in plotvars.keys():
    plotvars_to_write_out[key] = plotvars[key].copy()
    plotvars_to_write_out[key]['values'] = []

icuts_to_dump = [0,1,2,3,4]

cuts = []
ncuts = 5
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
        tag = name.split('basicPID_R24-AllEvents-')[1].split('-OnPeak-R24-')[0]
    else:
        # MC
        tag = 'SP-{0}'.format(name.split('SP-')[1].split('-R24')[0])
    return tag
################################################################################

outfilename = None
sptag = None
if outfilename is None:
    sptag = get_sptag(args.infiles[0][0]) 
    #outfilename = 'OUTPUT_{0}_{1}_nfiles{2}.pkl'.format(decay,sptag,len(args.infiles[0]))
    #print(outfilename)
    #exit()

    # Better names?
    fulldirName = '/data/physics/bellis/BaBar/rootfiles/cut_summary_files/{0}/{1}'.format(sptag,decay)
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
    outfilename = '{0}/OUTPUT_{1}_nfiles{2}.pkl'.format(fulldirName,ntag,len(args.infiles[0]))
    print(outfilename)
    #exit()



for i in range(nentries):

    if i%1000==0:
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


    # Should the low cut be 2.2 or 2.3? 
    cut1 = 1
    if decay=='pnu':
        cut1 = np==1 and pp[0]>2.3 and pp[0]<2.8 
        cut2 = ncharged>3
    elif decay=='nmu':
        cut1 = nmu==1 and mup[0]>2.3 and mup[0]<2.8 
        cut2 = ncharged>3
    elif decay=='ne':
        cut1 = ne==1 and ep[0]>2.3 and ep[0]<2.8
        cut2 = ncharged>3
    elif decay=='pmu' or decay=='pe':
        cut1 = nbnvbcand==1 and bnvprotp3[0]>2.3 and bnvlepp3[0]>2.3 and bnvprotp3[0]<2.8 and bnvlepp3[0]<2.8
        cut2 = ncharged>5


    if decay=='pnu' or decay=='nmu' or decay=='ne':
        cut3 = nhighmom==1
        cut4 = missingmom>1 and missingE>1 # These cuts seem to be correlated with tagmass and tagdeltaE
    elif decay=='pmu' or decay=='pe':
        cut3 = nhighmom==2
        cut4 = missingmom<2.6 and missingE<5 # These cuts seem to be correlated with tagmass and tagdeltaE

    cuts = [1, cut1, (cut2*cut1), (cut1*cut2*cut3), (cut1*cut2*cut3*cut4)]#, (cut1*cut2*cut3*cut4*cut5), (cut1*cut2*cut3*cut4*cut5*cut6)]
    for icut,cut in enumerate(cuts):
        if cut:
            #print(icut)
            plotvars["nbnvbcand"]["values"][icut].append(nbnvbcand)
            for k in range(nbnvbcand):
                plotvars["bnvbcandmass"]["values"][icut].append(bnvbcandmass[k])
                plotvars["bnvbcandMES"]["values"][icut].append(bnvbcandMES[k])
                plotvars["bnvbcandDeltaE"]["values"][icut].append(bnvbcandDeltaE[k])
                plotvars["bnvprotp3"]["values"][icut].append(bnvprotp3[k])
                plotvars["bnvlepp3"]["values"][icut].append(bnvlepp3[k])

            plotvars["tagbcandmass"]["values"][icut].append(tagbcandmass)
            plotvars["tagbcandMES"]["values"][icut].append(tagbcandMES)
            plotvars["tagbcandDeltaE"]["values"][icut].append(tagbcandDeltaE)
            plotvars["tagq"]["values"][icut].append(tagq)

            plotvars["r2"]["values"][icut].append(r2)
            plotvars["r2all"]["values"][icut].append(r2all)
            plotvars["thrustmag"]["values"][icut].append(thrustmag)
            plotvars["thrustmagall"]["values"][icut].append(thrustmagall)
            plotvars["thrustcosth"]["values"][icut].append(thrustcosth)
            plotvars["thrustcosthall"]["values"][icut].append(thrustcosthall)
            plotvars["sphericityall"]["values"][icut].append(sphericityall)

            plotvars["nphot"]["values"][icut].append(nphot)
            plotvars["ncharged"]["values"][icut].append(ncharged)

            plotvars["missingmass"]["values"][icut].append(missingmass)
            plotvars["missingmom"]["values"][icut].append(missingmom)
            plotvars["missingE"]["values"][icut].append(missingE)
            plotvars["scalarmomsum"]["values"][icut].append(scalarmomsum)

            plotvars["nhighmom"]["values"][icut].append(nhighmom)

            plotvars["np"]["values"][icut].append(np)
            plotvars["nmu"]["values"][icut].append(nmu)
            plotvars["ne"]["values"][icut].append(ne)

            for k in range(np):
                plotvars["pp"]["values"][icut].append(pp[k])
            for k in range(nmu):
                plotvars["mup"]["values"][icut].append(mup[k])
            for k in range(ne):
                plotvars["ep"]["values"][icut].append(ep[k])

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
