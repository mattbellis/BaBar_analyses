import numpy as np
import ROOT

import sys

import zipfile

import myPIDselector
from myPIDselector import *

eps = PIDselector("e")
pps = PIDselector("p")
pips = PIDselector("pi")
Kps = PIDselector("K")
mups = PIDselector("mu")

totx = []
toty = []
totz = []


#particles = ["mu","e","pi","K","p"]
particle_masses = [0.000511, 0.105, 0.139, 0.494, 0.938, 0]
particle_lunds = [11, 13, 211, 321, 2212, 22]

allparts = [{}, {}, {}]

for pl in particle_lunds:
    allparts[0][pl] = []
    allparts[1][pl] = []
    allparts[2][pl] = []

################################################################################
'''
def selectPID(eps,mups,pips,Kps,pps,verbose=False):
    #verbose = True
    max_pid = -1
    max_particle = -1
    for i,ps in enumerate([eps,mups,pips,Kps,pps]):
        if verbose:
            ps.PrintSelectors()
        pid = ps.HighestBitFraction()
        #print pid
        if pid>max_pid:
            max_pid = pid
            max_particle = i
    #print max_particle,particles[max_particle]
    return max_particle,max_pid
'''

################################################################################
def vec_mag(vec):
    mag = np.sqrt(vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2])
    return mag
################################################################################
def angle(vec0, vec1, returncos=False):
    mag0 = vec_mag(vec0)
    mag1 = vec_mag(vec1)

    costheta = (vec0[0]*vec1[0] + vec0[1]*vec1[1] + vec0[2]*vec1[2])/(mag0*mag1)

    if returncos:
        return costheta

    return np.arccos(costheta)
    
################################################################################
################################################################################

################################################################################
def selectPID(eps,mups,pips,Kps,pps,verbose=False):
    #verbose = True
    max_pid = 2 # Pion
    max_particle = -1

    s = mups.selectors
    #print(s)
    for i in s:
        #print(i)
        if i.find("BDT")>=0 and (i.find("TightMuon")>=0 or i.find("LooseMuon")>=0):
            if mups.IsSelectorSet(i):
                return 1,1.0 # Muon
    
    s = eps.selectors
    #print(s)
    for i in s:
        #print(i)
        if i.find("TightKM")>=0:
            if eps.IsSelectorSet(i):
                return 0,1.0 # Electron
    
    s = pps.selectors
    #print(s)
    for i in s:
        #print(i)
        #if i.find("SuperTightKM")>=0 or i.find("SuperTightKM")>=0:
        #if i.find("LooseKM")>=0 or i.find("TightKM")>=0:
        if i.find("LooseKM")==0 or i.find("TightKM")>=0:
            if pps.IsSelectorSet(i):
                return 4,1.0 # proton

    s = Kps.selectors
    #print(s)
    for i in s:
        #print(i)
        if i.find("Tight")>=0:
            if Kps.IsSelectorSet(i):
                return 3,1.0 # Kaon
    
    # Otherwise it is a pion
    
    return max_pid,max_particle
################################################################################

################################################################################
# Invariant Mass Function
################################################################################
def invmass(p4,return_squared=False):
    if type(p4[0]) != float:
        p4 = list(p4)

    totp4 = np.array([0., 0., 0., 0.])
    for p in p4:
        totp4[0] += p[0]
        totp4[1] += p[1]
        totp4[2] += p[2]
        totp4[3] += p[3]

    m2 = totp4[0]**2 - totp4[1]**2 - totp4[2]**2 - totp4[3]**2

    if return_squared:
        return m2

    m = -999
    if m2 >= 0:
        m = np.sqrt(m2)
    else:
        m = -np.sqrt(np.abs(m2))
    return m
################################################################################


################################################################################
def recalc_energy(mass,p3):
    energy = np.sqrt(mass*mass + vec_mag(p3)**2)
    return energy
################################################################################

################################################################################
def sph2cart(pmag,costh,phi):
    theta = np.arccos(costh)
    x = pmag*np.sin(theta)*np.cos(phi)
    y = pmag*np.sin(theta)*np.sin(phi)
    z = pmag*costh
    return x,y,z
################################################################################

#f = ROOT.TFile(sys.argv[1])
#f.ls()
#tree = f.Get("ntp1")

tree = ROOT.TChain("ntp1")
for infile in sys.argv[1:]:
    print(infile)
    tree.AddFile(infile)


#tree.Print()
#exit()
nentries = tree.GetEntries()
#nentries = 10000


#outfilename = "%s.dat" % (sys.argv[1].split('/')[-1].split('.root')[0])
#outfilename = "%s.dat" % (sys.argv[1].split('.root')[0])
#outfile = open(outfilename,'w')

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
outfilename = None
if outfilename is None:
    #outfilename = filenames[0].split('/')[-1].split('.root')[0] + "_OUTPUT.root"
    outfilename = sys.argv[1].split('.root')[0] + "_PID_skim.root"
outfile = ROOT.TFile(outfilename, "RECREATE")
outfile.cd()

outtree = ROOT.TTree("Tskim", "Our tree of everything")
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
pie = array('f', 64*[-1.])
outtree.Branch('pie', pie, 'pie[npi]/F')
pipx = array('f', 64*[-1.])
outtree.Branch('pipx', pipx, 'pipx[npi]/F')
pipy = array('f', 64*[-1.])
outtree.Branch('pipy', pipy, 'pipy[npi]/F')
pipz = array('f', 64*[-1.])
outtree.Branch('pipz', pipz, 'pipz[npi]/F')
piq = array('i', 64*[-1])
outtree.Branch('piq', piq, 'piq[npi]/I')
pipibit = array('i', 64*[-1])
outtree.Branch('pipibit', pipibit, 'pipibit[npi]/I')
pikbit = array('i', 64*[-1])
outtree.Branch('pikbit', pikbit, 'pikbit[npi]/I')
pipbit = array('i', 64*[-1])
outtree.Branch('pipbit', pipbit, 'pipbit[npi]/I')
piebit = array('i', 64*[-1])
outtree.Branch('piebit', piebit, 'piebit[npi]/I')
pimubit = array('i', 64*[-1])
outtree.Branch('pimubit', pimubit, 'pimubit[npi]/I')

nk = array('i', [-1])
outtree.Branch('nk', nk, 'nk/I')
ke = array('f', 64*[-1.])
outtree.Branch('ke', ke, 'ke[nk]/F')
kpx = array('f', 64*[-1.])
outtree.Branch('kpx', kpx, 'kpx[nk]/F')
kpy = array('f', 64*[-1.])
outtree.Branch('kpy', kpy, 'kpy[nk]/F')
kpz = array('f', 64*[-1.])
outtree.Branch('kpz', kpz, 'kpz[nk]/F')
kq = array('i', 64*[-1])
outtree.Branch('kq', kq, 'kq[nk]/I')
kpibit = array('i', 64*[-1])
outtree.Branch('kpibit', kpibit, 'kpibit[nk]/I')
kkbit = array('i', 64*[-1])
outtree.Branch('kkbit', kkbit, 'kkbit[nk]/I')
kpbit = array('i', 64*[-1])
outtree.Branch('kpbit', kpbit, 'kpbit[nk]/I')
kebit = array('i', 64*[-1])
outtree.Branch('kebit', kebit, 'kebit[nk]/I')
kmubit = array('i', 64*[-1])
outtree.Branch('kmubit', kmubit, 'kmubit[nk]/I')

nproton = array('i', [-1])
outtree.Branch('nproton', nproton, 'nproton/I')
protone = array('f', 64*[-1.])
outtree.Branch('protone', protone, 'protone[nproton]/F')
protonpx = array('f', 64*[-1.])
outtree.Branch('protonpx', protonpx, 'protonpx[nproton]/F')
protonpy = array('f', 64*[-1.])
outtree.Branch('protonpy', protonpy, 'protonpy[nproton]/F')
protonpz = array('f', 64*[-1.])
outtree.Branch('protonpz', protonpz, 'protonpz[nproton]/F')
protonq = array('i', 64*[-1])
outtree.Branch('protonq', protonq, 'protonq[nproton]/I')
protonpibit = array('i', 64*[-1])
outtree.Branch('protonpibit', protonpibit, 'protonpibit[nproton]/I')
protonkbit = array('i', 64*[-1])
outtree.Branch('protonkbit', protonkbit, 'protonkbit[nproton]/I')
protonpbit = array('i', 64*[-1])
outtree.Branch('protonpbit', protonpbit, 'protonpbit[nproton]/I')
protonebit = array('i', 64*[-1])
outtree.Branch('protonebit', protonebit, 'protonebit[nproton]/I')
protonmubit = array('i', 64*[-1])
outtree.Branch('protonmubit', protonmubit, 'protonmubit[nproton]/I')


ne = array('i', [-1])
outtree.Branch('ne', ne, 'ne/I')
ee = array('f', 64*[-1.])
outtree.Branch('ee', ee, 'ee[ne]/F')
epx = array('f', 64*[-1.])
outtree.Branch('epx', epx, 'epx[ne]/F')
epy = array('f', 64*[-1.])
outtree.Branch('epy', epy, 'epy[ne]/F')
epz = array('f', 64*[-1.])
outtree.Branch('epz', epz, 'epz[ne]/F')
eq = array('i', 64*[-1])
outtree.Branch('eq', eq, 'eq[ne]/I')
epibit = array('i', 64*[-1])
outtree.Branch('epibit', epibit, 'epibit[ne]/I')
ekbit = array('i', 64*[-1])
outtree.Branch('ekbit', ekbit, 'ekbit[ne]/I')
epbit = array('i', 64*[-1])
outtree.Branch('epbit', epbit, 'epbit[ne]/I')
eebit = array('i', 64*[-1])
outtree.Branch('eebit', eebit, 'eebit[ne]/I')
emubit = array('i', 64*[-1])
outtree.Branch('emubit', emubit, 'emubit[ne]/I')

nmu = array('i', [-1])
outtree.Branch('nmu', nmu, 'nmu/I')
mue = array('f', 64*[-1.])
outtree.Branch('mue', mue, 'mue[nmu]/F')
mupx = array('f', 64*[-1.])
outtree.Branch('mupx', mupx, 'mupx[nmu]/F')
mupy = array('f', 64*[-1.])
outtree.Branch('mupy', mupy, 'mupy[nmu]/F')
mupz = array('f', 64*[-1.])
outtree.Branch('mupz', mupz, 'mupz[nmu]/F')
muq = array('i', 64*[-1])
outtree.Branch('muq', muq, 'muq[nmu]/I')
mupibit = array('i', 64*[-1])
outtree.Branch('mupibit', mupibit, 'mupibit[nmu]/I')
mukbit = array('i', 64*[-1])
outtree.Branch('mukbit', mukbit, 'mukbit[nmu]/I')
mupbit = array('i', 64*[-1])
outtree.Branch('mupbit', mupbit, 'mupbit[nmu]/I')
muebit = array('i', 64*[-1])
outtree.Branch('muebit', muebit, 'muebit[nmu]/I')
mumubit = array('i', 64*[-1])
outtree.Branch('mumubit', mumubit, 'mumubit[nmu]/I')

ngamma = array('i', [-1])
outtree.Branch('ngamma', ngamma, 'ngamma/I')
gammae = array('f', 128*[-1.])
outtree.Branch('gammae', gammae, 'gammae[ngamma]/F')
gammapx = array('f', 128*[-1.])
outtree.Branch('gammapx', gammapx, 'gammapx[ngamma]/F')
gammapy = array('f', 128*[-1.])
outtree.Branch('gammapy', gammapy, 'gammapy[ngamma]/F')
gammapz = array('f', 128*[-1.])
outtree.Branch('gammapz', gammapz, 'gammapz[ngamma]/F')

for i in range(nentries):

    #myparticles = {"electrons":[], "muons":[], "pions":[], "kaons":[], "protons":[], "gammas":[]}
    #myparticles = [[], [], [], [], [], []]
    myparticles = []


    if i%1000==0:
        print(i,nentries)

    if i>100000000:
        break

    #output = "Event: %d\n" % (i)
    #output = ""
    tree.GetEntry(i)

    nvals = 0

    #beam = np.array([tree.eeE, tree.eePx, tree.eePy, tree.eePz, 0, 0])
    beamp4 = np.array([tree.eeE, tree.eePx, tree.eePy, tree.eePz])
    beammass = invmass([beamp4])
    beam = np.array([beammass, 0.0, 0.0, 0.0, 0, 0])

    beame[0] = tree.eeE
    beampx[0] = tree.eePx
    beampy[0] = tree.eePy
    beampz[0] = tree.eePz
    beamvtxx[0] = tree.xPrimaryVtx
    beamvtxy[0] = tree.yPrimaryVtx
    beamvtxz[0] = tree.zPrimaryVtx


    r2[0] = tree.R2
    r2all[0] = tree.R2All
    thrustmag[0] = tree.thrustMag
    thrustmagall[0] = tree.thrustMagAll
    thrustcosth[0] = tree.thrustCosTh
    thrustcosthall[0] = tree.thrustCosThAll
    sphericityall[0] = tree.sphericityAll

    matchIdx = -1
    LUNDTOMATCH = 211
    nmc = tree.mcLen
    #print("MC ----{0}----".format(nmc))
    bidx = []
    for j in range(nmc):
        #print(tree.mcLund[j], tree.mothIdx[j], tree.dauLen[j], tree.dauIdx[j])
        pid = abs(tree.mcLund[j])
        mothIdx = tree.mothIdx[j]
        if pid==511:
            bidx.append(j)
        if mothIdx in bidx:
            #print("B child: ",pid, j)
            if pid==LUNDTOMATCH:
                matchIdx = j

        
    leptons = []
    protons = []
    ntrks = tree.nTRK
    #print("----{0}----".format(ntrks))
    #print("{0} {1} {2} {3} {4}".format(tree.np, tree.nK, tree.npi, tree.ne, tree.nmu))
    npi[0] = 0
    nk[0] = 0
    nproton[0] = 0
    ne[0] = 0
    nmu[0] = 0
    for j in range(ntrks):
        idx = tree.TRKMCIdx[j]
        #print("idx,len: ",idx,tree.mcLen, ntrks)
        #print("track", j)
        ebit,mubit,pibit,Kbit,pbit = tree.eSelectorsMap[j],tree.muSelectorsMap[j],tree.piSelectorsMap[j],tree.KSelectorsMap[j],tree.pSelectorsMap[j]
        #print(ebit,mubit,pibit,Kbit,pbit)
        eps.SetBits(ebit); mups.SetBits(mubit); pips.SetBits(pibit); Kps.SetBits(Kbit); pps.SetBits(pbit);
        max_particle,max_pid = selectPID(eps,mups,pips,Kps,pps,verbose=True)
        #print(max_particle,max_pid)
        #e = tree.TRKenergy[j]
        #p3 = tree.TRKp3[j]
        #phi = tree.TRKphi[j]
        #costh = tree.TRKcosth[j]
        if idx>0:
            mcLund = abs(tree.mcLund[idx])
            if mcLund==LUNDTOMATCH: #or mcLund==13:
                #print("Matched! ",tree.TRKLund[j], idx, tree.mcLund[idx], max_particle,max_pid," -- ",ebit,mubit,pibit,Kbit,pbit)
                #print(idx,matchIdx)
                if idx==matchIdx:
                    match_max.append(max_particle)

        e = tree.TRKenergyCM[j]
        p3 = tree.TRKp3CM[j]
        phi = tree.TRKphiCM[j]
        costh = tree.TRKcosthCM[j]
        px,py,pz = sph2cart(p3,costh,phi)
        lund = tree.TRKLund[j]
        q = int(lund/np.abs(lund))

        mylund = particle_lunds[max_particle]

        new_energy = recalc_energy(particle_masses[max_particle],[px,py,pz])
        #print(lund,mylund,e, new_energy)
        particle = [new_energy,px,py,pz,q,mylund]
        myparticles.append(particle)


        if mylund==211:
            pie[npi[0]] = new_energy
            pipx[npi[0]] = px
            pipy[npi[0]] = py
            pipz[npi[0]] = pz
            piq[npi[0]] = q
            pipibit[npi[0]] = pibit
            pikbit[npi[0]] = Kbit
            pipbit[npi[0]] = pbit
            piebit[npi[0]] = ebit
            pimubit[npi[0]] = mubit
            npi[0] += 1
        elif mylund==321:
            ke[nk[0]] = new_energy
            kpx[nk[0]] = px
            kpy[nk[0]] = py
            kpz[nk[0]] = pz
            kq[nk[0]] = q
            kpibit[nk[0]] = pibit
            kkbit[nk[0]] = Kbit
            kpbit[nk[0]] = pbit
            kebit[nk[0]] = ebit
            kmubit[nk[0]] = mubit
            nk[0] += 1
        elif mylund==2212:
            protone[nproton[0]] = new_energy
            protonpx[nproton[0]] = px
            protonpy[nproton[0]] = py
            protonpz[nproton[0]] = pz
            protonq[nproton[0]] = q
            protonpibit[nproton[0]] = pibit
            protonkbit[nproton[0]] = Kbit
            protonpbit[nproton[0]] = pbit
            protonebit[nproton[0]] = ebit
            protonmubit[nproton[0]] = mubit
            nproton[0] += 1
        elif mylund==11:
            ee[ne[0]] = new_energy
            epx[ne[0]] = px
            epy[ne[0]] = py
            epz[ne[0]] = pz
            eq[ne[0]] = q
            epibit[ne[0]] = pibit
            ekbit[ne[0]] = Kbit
            epbit[ne[0]] = pbit
            eebit[ne[0]] = ebit
            emubit[ne[0]] = mubit
            ne[0] += 1
        elif mylund==13:
            mue[nmu[0]] = new_energy
            mupx[nmu[0]] = px
            mupy[nmu[0]] = py
            mupz[nmu[0]] = pz
            muq[nmu[0]] = q
            mupibit[nmu[0]] = pibit
            mukbit[nmu[0]] = Kbit
            mupbit[nmu[0]] = pbit
            muebit[nmu[0]] = ebit
            mumubit[nmu[0]] = mubit
            nmu[0] += 1



        pmag = vec_mag(particle[1:4])
        if (particle[-1]==11 or particle[-1]==13) and pmag>2.0 and pmag<3.0:
            leptons.append(np.array(particle + [j]))
        elif particle[-1]==2212 and pmag>2.0 and pmag<3.0:
            protons.append(np.array(particle + [j]))
    #exit()

    ############################################################################
    # Print out the photons
    ############################################################################
    ngamma[0] = 0
    nphotons = tree.ngamma
    #output += "%d\n" % (nphotons)
    for j in range(nphotons):
        #e = tree.gammaenergy[j]
        #p3 = tree.gammap3[j]
        #phi = tree.gammaphi[j]
        #costh = tree.gammacosth[j]
        e = tree.gammaenergyCM[j]
        p3 = tree.gammap3CM[j]
        phi = tree.gammaphiCM[j]
        costh = tree.gammacosthCM[j]
        px,py,pz = sph2cart(p3,costh,phi)

        new_energy = recalc_energy(0,[px,py,pz])
        #particle = [e,px,py,pz,0,22]
        particle = [new_energy,px,py,pz,0,22]
        myparticles.append(particle)

        if ngamma[0]<128:
            gammae[ngamma[0]] = new_energy
            gammapx[ngamma[0]] = px
            gammapy[ngamma[0]] = py
            gammapz[ngamma[0]] = pz
        ngamma[0] += 1

    # Missing mass?
    myparticles = np.array(myparticles)
    totp4 = beam[0:4]
    print(totp4)
    for p in myparticles:
        #print(totp4,p[0:4])
        totp4 -= p[0:4]
    #print(totp4)
    missingmass[0] = invmass([totp4],return_squared=True)
    #print(missingmass[0])

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



