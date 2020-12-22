import numpy as np
import ROOT

import sys
import argparse
import os

import zipfile

import myPIDselector
from myPIDselector import *

from babar_tools import vec_mag,angle,selectPID,invmass,recalc_energy,sph2cart
from babar_tools import particle_masses,particle_lunds
from babar_tools import eps,pps,pips,Kps,mups # The PID selectors for each particle
from babar_tools import calc_B_variables

parser = argparse.ArgumentParser(description='Process some files for B BNV search.')
parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
# decay can be pnu, ne, nmu
parser.add_argument('--decay', dest='decay', default="pnu", help='Decay to assume')
parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
args = parser.parse_args()

#print(args)
decay = args.decay


tree = ROOT.TChain("Tskim")
for infile in args.infiles[0]:
    print(infile)
    tree.AddFile(infile)


#tree.Print()
#exit()
nentries = tree.GetEntries()
#nentries = 10000

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

#filenames = sys.argv[1:]
outfilename = args.outfile
if outfilename is None:
    #outfilename = sys.argv[1].split('.root')[0] + "_KINVARS_" + decay + ".root"
    dirName = 'kinematic_distributions_' + decay
    fulldirName = '/'.join(sys.argv[1].split('/')[:-1]) + "/" + dirName
    try:
        # Create target Directory
        os.mkdir(fulldirName)
        print("Directory " , fulldirName ,  " Created ")
    except FileExistsError:
        print("Directory " , fulldirName ,  " already exists")
    #outfilename = filenames[0].split('/')[-1].split('.root')[0] + "_OUTPUT.root"
    #outfilename = sys.argv[1].split('.root')[0] + "_PID_skim.root"
    #outfilename = '/'.join(sys.argv[1].split('/')[:-1]) + "/" + dirName + "/" + sys.argv[1].split('/')[-1].split('.root')[0] + "_KINVARS_" + decay + ".root"
    outfilename = '/'.join(sys.argv[1].split('/')[:-1]) + "/" + dirName + "/" + sys.argv[1].split('/')[-1].split('.root')[0] + "_KINVARS.root"
    print(outfilename)
    #exit()

outfile = ROOT.TFile(outfilename, "RECREATE")
outfile.cd()

outtree = ROOT.TTree("analysis", "Our tree of everything")
# Add beam and shape info
# Add k, muon, electron, proton, photon

beame = array('f', [-1.])
outtree.Branch('beame', beame, 'beame/F')
beampx = array('f', [-1.])
outtree.Branch('beampx', beampx, 'beampx/F')
beampy = array('f', [-1.])
outtree.Branch('beampy', beampy, 'beampy/F')
beampz = array('f', [-1.])
outtree.Branch('beampz', beampz, 'beampz/F')
beamvtxx = array('f', [-1.])
outtree.Branch('beamvtxx', beamvtxx, 'beamvtxx/F')
beamvtxy = array('f', [-1.])
outtree.Branch('beamvtxy', beamvtxy, 'beamvtxy/F')
beamvtxz = array('f', [-1.])
outtree.Branch('beamvtxz', beamvtxz, 'beamvtxz/F')

missingmom = array('f', [-1.])
outtree.Branch('missingmom', missingmom, 'missingmom/F')
missingE = array('f', [-1.])
outtree.Branch('missingE', missingE, 'missingE/F')
scalarmomsum = array('f', [-1.])
outtree.Branch('scalarmomsum', scalarmomsum, 'scalarmomsum/F')

nhighmom = array('i', [-1])
outtree.Branch('nhighmom', nhighmom, 'nhighmom/I')
ntrks = array('i', [-1])
outtree.Branch('ntrks', ntrks, 'ntrks/I')

#bcand,dE,mes, tagbcand,tagdE,tagmes
nbnvbcand = array('i', [-1])
outtree.Branch('nbnvbcand', nbnvbcand, 'nbnvbcand/I')
bcand = array('f', 64*[-1.0])
outtree.Branch('bcand', bcand, 'bcand[nbnvbcand]/F')
dE = array('f', 64*[-1.0])
outtree.Branch('dE', dE, 'dE[nbnvbcand]/F')
mes = array('f', 64*[-1.0])
outtree.Branch('mes', mes, 'mes[nbnvbcand]/F')
bnvprotp3 = array('f', 64*[-1.0])
outtree.Branch('bnvprotp3', bnvprotp3, 'bnvprotp3[nbnvbcand]/F')
bnvprotcosth = array('f', 64*[-1.0])
outtree.Branch('bnvprotcosth', bnvprotcosth, 'bnvprotcosth[nbnvbcand]/F')
bnvlepp3 = array('f', 64*[-1.0])
outtree.Branch('bnvlepp3', bnvlepp3, 'bnvlepp3[nbnvbcand]/F')
bnvlepcosth = array('f', 64*[-1.0])
outtree.Branch('bnvlepcosth', bnvlepcosth, 'bnvlepcosth[nbnvbcand]/F')
bnvprotidx = array('i', 64*[-1])
outtree.Branch('bnvprotidx', bnvprotidx, 'bnvprotidx[nbnvbcand]/I')
bnvlepidx = array('i', 64*[-1])
outtree.Branch('bnvlepidx', bnvlepidx, 'bnvlepidx[nbnvbcand]/I')

tagbcand = array('f', 64*[-1.0])
outtree.Branch('tagbcand', tagbcand, 'tagbcand[nbnvbcand]/F')
tagdE = array('f', 64*[-1.0])
outtree.Branch('tagdE', tagdE, 'tagdE[nbnvbcand]/F')
tagmes = array('f', 64*[-1.0])
outtree.Branch('tagmes', tagmes, 'tagmes[nbnvbcand]/F')
tagq = array('f', 64*[-1.0])
outtree.Branch('tagq', tagq, 'tagq[nbnvbcand]/F')

missingmassES = array('f', 64*[-1.])
outtree.Branch('missingmassES', missingmassES, 'missingmassES[nbnvbcand]/F')
missingmass2 = array('f', 64*[-1.])
outtree.Branch('missingmass2', missingmass2, 'missingmass2[nbnvbcand]/F')


r2 = array('f', [-1.])
outtree.Branch('r2', r2, 'r2/F')
r2all = array('f', [-1.])
outtree.Branch('r2all', r2all, 'r2all/F')
thrustmag = array('f', [-1.])
outtree.Branch('thrustmag', thrustmag, 'thrustmag/F')
thrustmagall = array('f', [-1.])
outtree.Branch('thrustmagall', thrustmagall, 'thrustmagall/F')
thrustcosth = array('f', [-1.])
outtree.Branch('thrustcosth', thrustcosth, 'thrustcosth/F')
thrustcosthall = array('f', [-1.])
outtree.Branch('thrustcosthall', thrustcosthall, 'thrustcosthall/F')
sphericityall = array('f', [-1.])
outtree.Branch('sphericityall', sphericityall, 'sphericityall/F')

npi = array('i', [-1])
outtree.Branch('npi', npi, 'npi/I')

nk = array('i', [-1])
outtree.Branch('nk', nk, 'nk/I')

##################################################################
nproton = array('i', [-1])
outtree.Branch('nproton', nproton, 'nproton/I')
protone = array('f', 64*[-1.])
outtree.Branch('protone', protone, 'protone[nproton]/F')
protonp3 = array('f', 64*[-1.])
outtree.Branch('protonp3', protonp3, 'protonp3[nproton]/F')
protoncosth = array('f', 64*[-1.])
outtree.Branch('protoncosth', protoncosth, 'protoncosth[nproton]/F')
protonq = array('f', 64*[-1.])
outtree.Branch('protonq', protonq, 'protonq[nproton]/F')

protonIsTightKMProton = array('i', 64*[-1])
outtree.Branch('protonIsTightKMProton', protonIsTightKMProton, 'protonIsTightKMProton[nproton]/I')
protonIsVeryTightKMProton = array('i', 64*[-1])
outtree.Branch('protonIsVeryTightKMProton', protonIsVeryTightKMProton, 'protonIsVeryTightKMProton[nproton]/I')
protonIsSuperTightKMProton = array('i', 64*[-1])
outtree.Branch('protonIsSuperTightKMProton', protonIsSuperTightKMProton, 'protonIsSuperTightKMProton[nproton]/I')

protonIsTightKMKaon = array('i', 64*[-1])
outtree.Branch('protonIsTightKMKaon', protonIsTightKMKaon, 'protonIsTightKMKaon[nproton]/I')
protonIsVeryTightKMKaon = array('i', 64*[-1])
outtree.Branch('protonIsVeryTightKMKaon', protonIsVeryTightKMKaon, 'protonIsVeryTightKMKaon[nproton]/I')
protonIsSuperTightKMKaon = array('i', 64*[-1])
outtree.Branch('protonIsSuperTightKMKaon', protonIsSuperTightKMKaon, 'protonIsSuperTightKMKaon[nproton]/I')

protonIsTightBDTKaon = array('i', 64*[-1])
outtree.Branch('protonIsTightBDTKaon', protonIsTightBDTKaon, 'protonIsTightBDTKaon[nproton]/I')
protonIsVeryTightBDTKaon = array('i', 64*[-1])
outtree.Branch('protonIsVeryTightBDTKaon', protonIsVeryTightBDTKaon, 'protonIsVeryTightBDTKaon[nproton]/I')

protonIsTightKMPion = array('i', 64*[-1])
outtree.Branch('protonIsTightKMPion', protonIsTightKMPion, 'protonIsTightKMPion[nproton]/I')
protonIsVeryTightKMPion = array('i', 64*[-1])
outtree.Branch('protonIsVeryTightKMPion', protonIsVeryTightKMPion, 'protonIsVeryTightKMPion[nproton]/I')
protonIsSuperTightKMPion = array('i', 64*[-1])
outtree.Branch('protonIsSuperTightKMPion', protonIsSuperTightKMPion, 'protonIsSuperTightKMPion[nproton]/I')

protonIsTightKMElectron = array('i', 64*[-1])
outtree.Branch('protonIsTightKMElectron', protonIsTightKMElectron, 'protonIsTightKMElectron[nproton]/I')
protonIsVeryTightKMElectron = array('i', 64*[-1])
outtree.Branch('protonIsVeryTightKMElectron', protonIsVeryTightKMElectron, 'protonIsVeryTightKMElectron[nproton]/I')
protonIsSuperTightKMElectron = array('i', 64*[-1])
outtree.Branch('protonIsSuperTightKMElectron', protonIsSuperTightKMElectron, 'protonIsSuperTightKMElectron[nproton]/I')

protonIsBDTTightMuon = array('i', 64*[-1])
outtree.Branch('protonIsBDTTightMuon', protonIsBDTTightMuon, 'protonIsBDTTightMuon[nproton]/I')
protonIsBDTVeryTightMuon = array('i', 64*[-1])
outtree.Branch('protonIsBDTVeryTightMuon', protonIsBDTVeryTightMuon, 'protonIsBDTVeryTightMuon[nproton]/I')
protonIsBDTTightMuonFakeRate = array('i', 64*[-1])
outtree.Branch('protonIsBDTTightMuonFakeRate', protonIsBDTTightMuonFakeRate, 'protonIsBDTTightMuonFakeRate[nproton]/I')
protonIsBDTVeryTightMuonFakeRate = array('i', 64*[-1])
outtree.Branch('protonIsBDTVeryTightMuonFakeRate', protonIsBDTVeryTightMuonFakeRate, 'protonIsBDTVeryTightMuonFakeRate[nproton]/I')
##################################################################

##################################################################
ne = array('i', [-1])
outtree.Branch('ne', ne, 'ne/I')
ee = array('f', 64*[-1.])
outtree.Branch('ee', ee, 'ee[ne]/F')
ep3 = array('f', 64*[-1.])
outtree.Branch('ep3', ep3, 'ep3[ne]/F')
ecosth = array('f', 64*[-1.])
outtree.Branch('ecosth', ecosth, 'ecosth[ne]/F')
eq = array('f', 64*[-1.])
outtree.Branch('eq', eq, 'eq[ne]/F')

eIsTightKMProton = array('i', 64*[-1])
outtree.Branch('eIsTightKMProton', eIsTightKMProton, 'eIsTightKMProton[ne]/I')
eIsVeryTightKMProton = array('i', 64*[-1])
outtree.Branch('eIsVeryTightKMProton', eIsVeryTightKMProton, 'eIsVeryTightKMProton[ne]/I')
eIsSuperTightKMProton = array('i', 64*[-1])
outtree.Branch('eIsSuperTightKMProton', eIsSuperTightKMProton, 'eIsSuperTightKMProton[ne]/I')

eIsTightKMKaon = array('i', 64*[-1])
outtree.Branch('eIsTightKMKaon', eIsTightKMKaon, 'eIsTightKMKaon[ne]/I')
eIsVeryTightKMKaon = array('i', 64*[-1])
outtree.Branch('eIsVeryTightKMKaon', eIsVeryTightKMKaon, 'eIsVeryTightKMKaon[ne]/I')
eIsSuperTightKMKaon = array('i', 64*[-1])
outtree.Branch('eIsSuperTightKMKaon', eIsSuperTightKMKaon, 'eIsSuperTightKMKaon[ne]/I')

eIsTightBDTKaon = array('i', 64*[-1])
outtree.Branch('eIsTightBDTKaon', eIsTightBDTKaon, 'eIsTightBDTKaon[ne]/I')
eIsVeryTightBDTKaon = array('i', 64*[-1])
outtree.Branch('eIsVeryTightBDTKaon', eIsVeryTightBDTKaon, 'eIsVeryTightBDTKaon[ne]/I')

eIsTightKMPion = array('i', 64*[-1])
outtree.Branch('eIsTightKMPion', eIsTightKMPion, 'eIsTightKMPion[ne]/I')
eIsVeryTightKMPion = array('i', 64*[-1])
outtree.Branch('eIsVeryTightKMPion', eIsVeryTightKMPion, 'eIsVeryTightKMPion[ne]/I')
eIsSuperTightKMPion = array('i', 64*[-1])
outtree.Branch('eIsSuperTightKMPion', eIsSuperTightKMPion, 'eIsSuperTightKMPion[ne]/I')

eIsTightKMElectron = array('i', 64*[-1])
outtree.Branch('eIsTightKMElectron', eIsTightKMElectron, 'eIsTightKMElectron[ne]/I')
eIsVeryTightKMElectron = array('i', 64*[-1])
outtree.Branch('eIsVeryTightKMElectron', eIsVeryTightKMElectron, 'eIsVeryTightKMElectron[ne]/I')
eIsSuperTightKMElectron = array('i', 64*[-1])
outtree.Branch('eIsSuperTightKMElectron', eIsSuperTightKMElectron, 'eIsSuperTightKMElectron[ne]/I')

eIsBDTTightMuon = array('i', 64*[-1])
outtree.Branch('eIsBDTTightMuon', eIsBDTTightMuon, 'eIsBDTTightMuon[ne]/I')
eIsBDTVeryTightMuon = array('i', 64*[-1])
outtree.Branch('eIsBDTVeryTightMuon', eIsBDTVeryTightMuon, 'eIsBDTVeryTightMuon[ne]/I')
eIsBDTTightMuonFakeRate = array('i', 64*[-1])
outtree.Branch('eIsBDTTightMuonFakeRate', eIsBDTTightMuonFakeRate, 'eIsBDTTightMuonFakeRate[ne]/I')
eIsBDTVeryTightMuonFakeRate = array('i', 64*[-1])
outtree.Branch('eIsBDTVeryTightMuonFakeRate', eIsBDTVeryTightMuonFakeRate, 'eIsBDTVeryTightMuonFakeRate[ne]/I')
##################################################################


##################################################################
nmu = array('i', [-1])
outtree.Branch('nmu', nmu, 'nmu/I')
mue = array('f', 64*[-1.])
outtree.Branch('mue', mue, 'mue[nmu]/F')
mup3 = array('f', 64*[-1.])
outtree.Branch('mup3', mup3, 'mup3[nmu]/F')
mucosth = array('f', 64*[-1.])
outtree.Branch('mucosth', mucosth, 'mucosth[nmu]/F')
muq = array('f', 64*[-1.])
outtree.Branch('muq', muq, 'muq[nmu]/F')

muIsTightKMProton = array('i', 64*[-1])
outtree.Branch('muIsTightKMProton', muIsTightKMProton, 'muIsTightKMProton[nmu]/I')
muIsVeryTightKMProton = array('i', 64*[-1])
outtree.Branch('muIsVeryTightKMProton', muIsVeryTightKMProton, 'muIsVeryTightKMProton[nmu]/I')
muIsSuperTightKMProton = array('i', 64*[-1])
outtree.Branch('muIsSuperTightKMProton', muIsSuperTightKMProton, 'muIsSuperTightKMProton[nmu]/I')

muIsTightKMKaon = array('i', 64*[-1])
outtree.Branch('muIsTightKMKaon', muIsTightKMKaon, 'muIsTightKMKaon[nmu]/I')
muIsVeryTightKMKaon = array('i', 64*[-1])
outtree.Branch('muIsVeryTightKMKaon', muIsVeryTightKMKaon, 'muIsVeryTightKMKaon[nmu]/I')
muIsSuperTightKMKaon = array('i', 64*[-1])
outtree.Branch('muIsSuperTightKMKaon', muIsSuperTightKMKaon, 'muIsSuperTightKMKaon[nmu]/I')

muIsTightBDTKaon = array('i', 64*[-1])
outtree.Branch('muIsTightBDTKaon', muIsTightBDTKaon, 'muIsTightBDTKaon[nmu]/I')
muIsVeryTightBDTKaon = array('i', 64*[-1])
outtree.Branch('muIsVeryTightBDTKaon', muIsVeryTightBDTKaon, 'muIsVeryTightBDTKaon[nmu]/I')

muIsTightKMPion = array('i', 64*[-1])
outtree.Branch('muIsTightKMPion', muIsTightKMPion, 'muIsTightKMPion[nmu]/I')
muIsVeryTightKMPion = array('i', 64*[-1])
outtree.Branch('muIsVeryTightKMPion', muIsVeryTightKMPion, 'muIsVeryTightKMPion[nmu]/I')
muIsSuperTightKMPion = array('i', 64*[-1])
outtree.Branch('muIsSuperTightKMPion', muIsSuperTightKMPion, 'muIsSuperTightKMPion[nmu]/I')

muIsTightKMElectron = array('i', 64*[-1])
outtree.Branch('muIsTightKMElectron', muIsTightKMElectron, 'muIsTightKMElectron[nmu]/I')
muIsVeryTightKMElectron = array('i', 64*[-1])
outtree.Branch('muIsVeryTightKMElectron', muIsVeryTightKMElectron, 'muIsVeryTightKMElectron[nmu]/I')
muIsSuperTightKMElectron = array('i', 64*[-1])
outtree.Branch('muIsSuperTightKMElectron', muIsSuperTightKMElectron, 'muIsSuperTightKMElectron[nmu]/I')

muIsBDTTightMuon = array('i', 64*[-1])
outtree.Branch('muIsBDTTightMuon', muIsBDTTightMuon, 'muIsBDTTightMuon[nmu]/I')
muIsBDTVeryTightMuon = array('i', 64*[-1])
outtree.Branch('muIsBDTVeryTightMuon', muIsBDTVeryTightMuon, 'muIsBDTVeryTightMuon[nmu]/I')
muIsBDTTightMuonFakeRate = array('i', 64*[-1])
outtree.Branch('muIsBDTTightMuonFakeRate', muIsBDTTightMuonFakeRate, 'muIsBDTTightMuonFakeRate[nmu]/I')
muIsBDTVeryTightMuonFakeRate = array('i', 64*[-1])
outtree.Branch('muIsBDTVeryTightMuonFakeRate', muIsBDTVeryTightMuonFakeRate, 'muIsBDTVeryTightMuonFakeRate[nmu]/I')
##################################################################

ngamma = array('i', [-1])
outtree.Branch('ngamma', ngamma, 'ngamma/I')

for i in range(nentries):

    #myparticles = {"electrons":[], "muons":[], "pions":[], "kaons":[], "protons":[], "gammas":[]}
    #myparticles = [[], [], [], [], [], []]
    myparticles = []
    nhighmom[0] = 0
    scalarmomsum[0] = 0


    if i%1000==0:
        print(i,nentries)

    if i>100000000:
        break

    #output = "Event: %d\n" % (i)
    #output = ""
    tree.GetEntry(i)

    nvals = 0

    beamp4 = np.array([tree.beame, tree.beampx, tree.beampy, tree.beampz])
    beammass = invmass([beamp4])
    beam = np.array([beammass, 0.0, 0.0, 0.0, 0, 0, 0])
    #print("BEAM: ",beam)

    r2[0] = tree.r2
    r2all[0] = tree.r2all
    thrustmag[0] = tree.thrustmag
    thrustmagall[0] = tree.thrustmagall
    thrustcosth[0] = tree.thrustcosth
    thrustcosthall[0] = tree.thrustcosthall
    sphericityall[0] = tree.sphericityall

        
    npi[0] = tree.npi
    nk[0] = tree.nk
    nproton[0] = tree.nproton
    ne[0] = tree.ne
    nmu[0] = tree.nmu
    ngamma[0] = tree.ngamma

    highmomE = 0
    n_high_p = 0
    ntrks[0] = 0

    # Pions
    for j in range(npi[0]):

        ntrks[0] += 1

        e = tree.pie[j]
        px,py,pz = tree.pipx[j], tree.pipy[j], tree.pipz[j]
        q = tree.piq[j]

        particle = [e,px,py,pz,q,j,211]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        costh = particle[3]/p3
        scalarmomsum[0] += p3

        if p3>2.0:
            n_high_p += 1
            nhighmom[0] += 1
            highmomE += e

    # Kaons
    for j in range(nk[0]):

        ntrks[0] += 1

        e = tree.ke[j]
        px,py,pz = tree.kpx[j], tree.kpy[j], tree.kpz[j]
        q = tree.kq[j]

        particle = [e,px,py,pz,q,j,321]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        costh = particle[3]/p3
        scalarmomsum[0] += p3

        if p3>2.0:
            n_high_p += 1
            nhighmom[0] += 1
            highmomE += e

    # Protons
    for j in range(nproton[0]):

        ntrks[0] += 1

        e = tree.protone[j]
        px,py,pz = tree.protonpx[j], tree.protonpy[j], tree.protonpz[j]
        q = tree.protonq[j]
        pbit = tree.protonpbit[j]
        Kbit = tree.protonkbit[j]
        pibit = tree.protonpibit[j]
        ebit = tree.protonebit[j]
        mubit = tree.protonmubit[j]
        eps.SetBits(ebit); mups.SetBits(mubit); pips.SetBits(pibit); Kps.SetBits(Kbit); pps.SetBits(pbit);
        protonIsTightKMProton[j] = int(pps.IsBitSet(15))
        protonIsVeryTightKMProton[j] = int(pps.IsBitSet(16))
        protonIsSuperTightKMProton[j] = int(pps.IsBitSet(17))

        protonIsTightBDTKaon[j] = int(Kps.IsBitSet(22))
        protonIsVeryTightBDTKaon[j] = int(Kps.IsBitSet(23))

        protonIsTightKMKaon[j] = int(Kps.IsBitSet(27))
        protonIsVeryTightKMKaon[j] = int(Kps.IsBitSet(28))
        protonIsSuperTightKMKaon[j] = int(Kps.IsBitSet(29))

        protonIsTightKMPion[j] = int(pips.IsBitSet(13))
        protonIsVeryTightKMPion[j] = int(pips.IsBitSet(14))
        protonIsSuperTightKMPion[j] = int(pips.IsBitSet(15))

        protonIsTightKMElectron[j] = int(eps.IsBitSet(9))
        protonIsVeryTightKMElectron[j] = int(eps.IsBitSet(10))
        protonIsSuperTightKMElectron[j] = int(eps.IsBitSet(11))

        protonIsBDTTightMuon[j] = int(mups.IsBitSet(18))
        protonIsBDTVeryTightMuon[j] = int(mups.IsBitSet(19))
        protonIsBDTTightMuonFakeRate[j] = int(mups.IsBitSet(22))
        protonIsBDTVeryTightMuonFakeRate[j] = int(mups.IsBitSet(23))

        particle = [e,px,py,pz,q,j,2212]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        costh = particle[3]/p3
        scalarmomsum[0] += p3
        protone[j],protonp3[j],protoncosth[j],protonq[j] = e,p3,costh,q

        if p3>2.0:
            n_high_p += 1
            nhighmom[0] += 1
            highmomE += e

    # Muons
    for j in range(nmu[0]):

        ntrks[0] += 1

        e = tree.mue[j]
        px,py,pz = tree.mupx[j], tree.mupy[j], tree.mupz[j]
        q = tree.muq[j]
        pbit = tree.mupbit[j]
        Kbit = tree.mukbit[j]
        pibit = tree.mupibit[j]
        ebit = tree.muebit[j]
        mubit = tree.mumubit[j]
        eps.SetBits(ebit); mups.SetBits(mubit); pips.SetBits(pibit); Kps.SetBits(Kbit); pps.SetBits(pbit);
        muIsTightKMProton[j] = int(pps.IsBitSet(15))
        muIsVeryTightKMProton[j] = int(pps.IsBitSet(16))
        muIsSuperTightKMProton[j] = int(pps.IsBitSet(17))

        muIsTightBDTKaon[j] = int(Kps.IsBitSet(22))
        muIsVeryTightBDTKaon[j] = int(Kps.IsBitSet(23))

        muIsTightKMKaon[j] = int(Kps.IsBitSet(27))
        muIsVeryTightKMKaon[j] = int(Kps.IsBitSet(28))
        muIsSuperTightKMKaon[j] = int(Kps.IsBitSet(29))

        muIsTightKMPion[j] = int(pips.IsBitSet(13))
        muIsVeryTightKMPion[j] = int(pips.IsBitSet(14))
        muIsSuperTightKMPion[j] = int(pips.IsBitSet(15))

        muIsTightKMElectron[j] = int(eps.IsBitSet(9))
        muIsVeryTightKMElectron[j] = int(eps.IsBitSet(10))
        muIsSuperTightKMElectron[j] = int(eps.IsBitSet(11))

        muIsBDTTightMuon[j] = int(mups.IsBitSet(18))
        muIsBDTVeryTightMuon[j] = int(mups.IsBitSet(19))
        muIsBDTTightMuonFakeRate[j] = int(mups.IsBitSet(22))
        muIsBDTVeryTightMuonFakeRate[j] = int(mups.IsBitSet(23))


        particle = [e,px,py,pz,q,j,13]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        costh = particle[3]/p3
        scalarmomsum[0] += p3
        mue[j],mup3[j],mucosth[j],muq[j] = e,p3,costh,q

        if p3>2.0:
            n_high_p += 1
            nhighmom[0] += 1
            highmomE += e

    # Electrons
    for j in range(ne[0]):

        ntrks[0] += 1

        e = tree.ee[j]
        px,py,pz = tree.epx[j], tree.epy[j], tree.epz[j]
        q = tree.eq[j]
        pbit = tree.epbit[j]
        Kbit = tree.ekbit[j]
        pibit = tree.epibit[j]
        ebit = tree.eebit[j]
        mubit = tree.emubit[j]
        eps.SetBits(ebit); mups.SetBits(mubit); pips.SetBits(pibit); Kps.SetBits(Kbit); pps.SetBits(pbit);
        eIsTightKMProton[j] = int(pps.IsBitSet(15))
        eIsVeryTightKMProton[j] = int(pps.IsBitSet(16))
        eIsSuperTightKMProton[j] = int(pps.IsBitSet(17))

        eIsTightBDTKaon[j] = int(Kps.IsBitSet(22))
        eIsVeryTightBDTKaon[j] = int(Kps.IsBitSet(23))

        eIsTightKMKaon[j] = int(Kps.IsBitSet(27))
        eIsVeryTightKMKaon[j] = int(Kps.IsBitSet(28))
        eIsSuperTightKMKaon[j] = int(Kps.IsBitSet(29))

        eIsTightKMPion[j] = int(pips.IsBitSet(13))
        eIsVeryTightKMPion[j] = int(pips.IsBitSet(14))
        eIsSuperTightKMPion[j] = int(pips.IsBitSet(15))

        eIsTightKMElectron[j] = int(eps.IsBitSet(9))
        eIsVeryTightKMElectron[j] = int(eps.IsBitSet(10))
        eIsSuperTightKMElectron[j] = int(eps.IsBitSet(11))

        eIsBDTTightMuon[j] = int(mups.IsBitSet(18))
        eIsBDTVeryTightMuon[j] = int(mups.IsBitSet(19))
        eIsBDTTightMuonFakeRate[j] = int(mups.IsBitSet(22))
        eIsBDTVeryTightMuonFakeRate[j] = int(mups.IsBitSet(23))



        particle = [e,px,py,pz,q,j,11]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        costh = particle[3]/p3
        scalarmomsum[0] += p3
        ee[j],ep3[j],ecosth[j],eq[j] = e,p3,costh,q

        if p3>2.0:
            n_high_p += 1
            nhighmom[0] += 1
            highmomE += e

    # Gamma
    #print(ngamma[0])
    for j in range(ngamma[0]):

        e = tree.gammae[j]
        px,py,pz = tree.gammapx[j], tree.gammapy[j], tree.gammapz[j]

        particle = [e,px,py,pz,0,j,0]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        scalarmomsum[0] += p3

        if p3>2.0:
            n_high_p += 1
            nhighmom[0] += 1
            highmomE += e


    # Missing mass?
    myparticles = np.array(myparticles)
    '''
    totp4 = beam[0:4].copy()
    #print(totp4)
    for p in myparticles:
        #print(totp4,p[0:4])
        totp4 -= p[0:4]
    #print(totp4)
    missingmom[0] = vec_mag(totp4[1:])
    missingE[0] = totp4[0]

    # Recalculate the missing mass assuming B on one side 
    totp4[0] = beam[0]/2 - highmomE
    missingmass[0] = invmass([totp4],return_squared=True)

    #print(missingmass[0])
    #print(n_high_p)
    '''

    # Fill the bcandidates
    #print("====================")
    #print("# tracks!: ", ne[0],nmu[0],npi[0],nk[0],nproton[0], ne[0]+nmu[0]+npi[0]+nk[0]+nproton[0])
    nbnvbcand[0],temp_bcand,temp_dE,temp_mes,temp_bnvprotp3,temp_bnvlepp3,temp_bnvprotcosth,temp_bnvlepcosth,temp_bnvprotidx,temp_bnvlepidx, temp_tagbcand,temp_tagdE,temp_tagmes,temp_tagq,missingmom[0],missingE[0],temp_missingmass2,temp_missingmassES = calc_B_variables(myparticles,beam,decay)
    #print("nbnvbcand: ",nbnvbcand[0])
    for n in range(nbnvbcand[0]):
        bcand[n] = temp_bcand[n]
        dE[n] = temp_dE[n]
        mes[n] = temp_mes[n]
        bnvprotp3[n] = temp_bnvprotp3[n]
        bnvlepp3[n] = temp_bnvlepp3[n]
        bnvprotcosth[n] = temp_bnvprotcosth[n]
        bnvlepcosth[n] = temp_bnvlepcosth[n]
        bnvprotidx[n] = int(temp_bnvprotidx[n])
        bnvlepidx[n] = int(temp_bnvlepidx[n])

        tagbcand[n] = temp_tagbcand[n]
        tagdE[n] = temp_tagdE[n]
        tagmes[n] = temp_tagmes[n]
        tagq[n] = temp_tagq[n]
        missingmass2[n] = temp_missingmass2[n]
        missingmassES[n] = temp_missingmassES[n]
        #bnvlepidx[n] = int(temp_bnvlepidx[n])
        #bnvlepidx[n] = int(temp_bnvlepidx[n])


    #print(tagbcand)
    #print(missingmass[0])
    #print(bcand[0],dE[0],mes[0], tagbcand[0],tagdE[0],tagmes[0],missingmom[0],missingE[0],missingmass[0])
    #exit()

    #print(len(leptons),len(protons),nproton[0])
    # Use this for SP-9445 and SP-9446, p mu/e
    #flag = len(leptons)>0 and len(protons)>0
    flag = 1
    # SP-11975, B --> p neutrino
    #flag = len(leptons)==0 and len(protons)>0
    if flag:
        #print("FILLING!!!!!!!!!!!")
        outtree.Fill()

outfile.cd()
outfile.Write()
outfile.Close()



