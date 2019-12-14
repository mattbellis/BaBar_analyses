import numpy as np
import ROOT

import sys
import argparse


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

decay = args.decay


tree = ROOT.TChain("Tskim")
for infile in sys.argv[1:]:
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
    #outfilename = filenames[0].split('/')[-1].split('.root')[0] + "_OUTPUT.root"
    outfilename = sys.argv[1].split('.root')[0] + "_KINVARS_" + decay + ".root"
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

missingmass = array('f', [-1.])
outtree.Branch('missingmass', missingmass, 'missingmass/F')
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
bcand = array('f', [-1.0])
outtree.Branch('bcand', bcand, 'bcand/F')
dE = array('f', [-1.0])
outtree.Branch('dE', dE, 'dE/F')
mes = array('f', [-1.0])
outtree.Branch('mes', mes, 'mes/F')
tagbcand = array('f', [-1.0])
outtree.Branch('tagbcand', tagbcand, 'tagbcand/F')
tagdE = array('f', [-1.0])
outtree.Branch('tagdE', tagdE, 'tagdE/F')
tagmes = array('f', [-1.0])
outtree.Branch('tagmes', tagmes, 'tagmes/F')
tagq = array('f', [-1.0])
outtree.Branch('tagq', tagq, 'tagq/F')

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

nproton = array('i', [-1])
outtree.Branch('nproton', nproton, 'nproton/I')
protone = array('f', 64*[-1.])
outtree.Branch('protone', protone, 'protone[nproton]/F')
protonp3 = array('f', 64*[-1.])
outtree.Branch('protonp3', protonp3, 'protonp3[nproton]/F')
protonq = array('f', 64*[-1.])
outtree.Branch('protonq', protonq, 'protonq[nproton]/F')


ne = array('i', [-1])
outtree.Branch('ne', ne, 'ne/I')
ee = array('f', 64*[-1.])
outtree.Branch('ee', ee, 'ee[ne]/F')
ep3 = array('f', 64*[-1.])
outtree.Branch('ep3', ep3, 'ep3[ne]/F')
eq = array('f', 64*[-1.])
outtree.Branch('eq', eq, 'eq[ne]/F')


nmu = array('i', [-1])
outtree.Branch('nmu', nmu, 'nmu/I')
mue = array('f', 64*[-1.])
outtree.Branch('mue', mue, 'mue[nmu]/F')
mup3 = array('f', 64*[-1.])
outtree.Branch('mup3', mup3, 'mup3[nmu]/F')
muq = array('f', 64*[-1.])
outtree.Branch('muq', muq, 'muq[nmu]/F')


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
    beam = np.array([beammass, 0.0, 0.0, 0.0, 0, 0])
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

        particle = [e,px,py,pz,q,211]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
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

        particle = [e,px,py,pz,q,321]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
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

        particle = [e,px,py,pz,q,2212]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        scalarmomsum[0] += p3
        protone[j],protonp3[j],protonq[j] = e,p3,q

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

        particle = [e,px,py,pz,q,13]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        scalarmomsum[0] += p3
        mue[j],mup3[j],muq[j] = e,p3,q

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

        particle = [e,px,py,pz,q,11]
        myparticles.append(particle)
        p3 = vec_mag(particle[1:4])
        scalarmomsum[0] += p3
        ee[j],ep3[j],eq[j] = e,p3,q

        if p3>2.0:
            n_high_p += 1
            nhighmom[0] += 1
            highmomE += e

    # Gamma
    #print(ngamma[0])
    for j in range(ngamma[0]):

        e = tree.gammae[j]
        px,py,pz = tree.gammapx[j], tree.gammapy[j], tree.gammapz[j]

        particle = [e,px,py,pz,0,0]
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

    bcand[0],dE[0],mes[0], tagbcand[0],tagdE[0],tagmes[0],tagq[0],missingmom[0],missingE[0],missingmass[0] = calc_B_variables(myparticles,beam,decay)
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



