import numpy as np
import matplotlib.pylab as plt

import ROOT

import sys

import zipfile

import myPIDselector
from myPIDselector import *

import lichen.lichen as lch

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
        if i.find("LooseKM")>=0 or i.find("TightKM")>=0:
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
def invmass(p4):
    if type(p4[0]) != float:
        p4 = list(p4)

    totp4 = np.array([0., 0., 0., 0.])
    for p in p4:
        totp4[0] += p[0]
        totp4[1] += p[1]
        totp4[2] += p[2]
        totp4[3] += p[3]

    m2 = totp4[0]**2 - totp4[1]**2 - totp4[2]**2 - totp4[3]**2

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

f = ROOT.TFile(sys.argv[1])

f.ls()

tree = f.Get("ntp1")

#tree.Print()

#exit()

nentries = tree.GetEntries()

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

for i in range(nentries):

    #myparticles = {"electrons":[], "muons":[], "pions":[], "kaons":[], "protons":[], "gammas":[]}
    #myparticles = [[], [], [], [], [], []]
    myparticles = []


    if i%1000==0:
        print(i,nentries)

    if i>100000:
        break

    output = "Event: %d\n" % (i)
    #output = ""
    tree.GetEntry(i)

    nvals = 0

    #beam = np.array([tree.eeE, tree.eePx, tree.eePy, tree.eePz, 0, 0])
    beamp4 = np.array([tree.eeE, tree.eePx, tree.eePy, tree.eePz])
    beammass = invmass([beamp4])
    beam = np.array([beammass, 0.0, 0.0, 0.0, 0, 0])

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

        new_energy = recalc_energy(particle_masses[max_particle],[px,py,pz])
        particle = [new_energy,px,py,pz,q,particle_lunds[max_particle]]
        myparticles.append(particle)

        pmag = vec_mag(particle[1:4])
        if particle[-1]==11 and pmag>2.25 and pmag<2.8:
            leptons.append(np.array(particle + [j]))
        elif particle[-1]==2212 and pmag>2.25 and pmag<2.8:
            protons.append(np.array(particle + [j]))
    #exit()

    ############################################################################
    # Print out the photons
    ############################################################################
    nphotons = tree.ngamma
    output += "%d\n" % (nphotons)
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

        for electron in leptons:
            ang = angle(electron[1:4],particle[1:4])#,returncos=True)
            angles.append(ang)

            # Add Brehm photons
            # WHAT IF PHOTON IS CLOSE TO TWO OR MORE leptons????
            #'''
            #if ang>=0.9958: # Do this for cos
            #if ang<=0.20:
            if ang<=0.05:
                #print(electron)
                electron[0:4] += particle[0:4]
                #print(electron)
            else:
                myparticles.append(particle)
            #'''

    myparticles = np.array(myparticles)

    #print(myparticles)
    tot = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    tot += beam

    tpart = myparticles.transpose()
    pids = tpart[-1]
    qs = tpart[-2]
    '''
    print("pids: ",pids)
    print("qs:   ",qs)
    print(len(pids[pids==2212]))
    print(qs.sum())
    '''

    totq = 0
    nbcand = 0
    for proton in protons:
        for lepton in leptons:

            # Make sure the charges are not the same
            if proton[4] == lepton[4]:
                continue

            p = vec_mag(proton[1:4])
            prot_p.append(p)
            p = vec_mag(lepton[1:4])
            lep_p.append(p)

            # B candidates
            bc = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            tagbc = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

            bc = proton[0:-1] + lepton[0:-1]

            pidx = proton[-1]
            lidx = lepton[-1]
            
            # Get the tag side and don't count the proton or lepton
            for k,p in enumerate(myparticles):
                if k!=pidx and k!=lidx:
                    totq += p[4]
                    tagbc += p

            bcand.append(invmass([bc]))
            dE = bc[0] - beam[0]/2.0
            bc[0] = beam[0]/2.0
            mes = invmass([bc])
            bcandMES.append(mes)
            bcandDeltaE.append(dE)
            bcandMM.append(invmass([beam-bc]))

            tagbcand.append(invmass([tagbc]))
            tagdE = tagbc[0] - beam[0]/2.0
            tagbc[0] = beam[0]/2.0
            tagmes = invmass([tagbc])
            tagbcandMES.append(tagmes)
            tagbcandDeltaE.append(tagdE)
            tagbcandMM.append(invmass([beam-tagbc]))

            nbcand += 1
        
    totqs.append(totq)
    nbcands.append(nbcand)

plt.figure()
plt.hist(match_max,bins=5,range=(0,5))

# Brehm at 0.9958 in cos(theta)?
plt.figure()
plt.subplot(3,3,1)
plt.hist(angles,bins=1000)

#plt.show()
#exit()

plt.subplot(3,3,2)
plt.hist(prot_p,bins=100)
plt.subplot(3,3,3)
plt.hist(lep_p,bins=100)

plt.subplot(3,3,4)
plt.hist(totqs,bins=52,range=(-5,5))

plt.subplot(3,3,5)
plt.hist(nbcands,bins=7,range=(-1,6))

plt.tight_layout()


###################
plt.figure(figsize=(8,3))
plt.subplot(1,2,1)
lch.hist_err(bcandMES,bins=200,range=(5.2,5.3))
#lch.hist_err(bcandMES,bins=200,range=(0,5.3))
plt.xlabel(r'M$_{\rm ES}$ [GeV/c$^{2}$]',fontsize=18)

plt.subplot(1,2,2)
lch.hist_err(bcandDeltaE,bins=200,range=(-0.2,0.2))
#lch.hist_err(bcandDeltaE,bins=200,range=(-10,10))
plt.xlabel(r'$\Delta$E [GeV]',fontsize=18)

plt.tight_layout()

###################
plt.figure()
plt.subplot(3,3,1)
plt.hist(bcand,bins=200,range=(0,15))
plt.xlabel(r'B-cand mass [GeV/c$^{2}$]',fontsize=10)
    
plt.subplot(3,3,2)
#plt.hist(bcandMES,bins=200,range=(2,7))
plt.hist(bcandMES,bins=200,range=(5,5.3))
plt.xlabel(r'M$_{\rm ES}$ [GeV/c$^{2}$]',fontsize=10)

plt.subplot(3,3,3)
plt.hist(bcandDeltaE,bins=200,range=(-1,1))
plt.xlabel(r'$\Delta$E [GeV]',fontsize=10)

plt.subplot(3,3,4)
#plt.hist(bcandMM,bins=200,range=(2,7))
plt.hist(bcandMM,bins=200,range=(-5,7))
plt.xlabel(r'Missing mass [GeV/c$^{2}$]',fontsize=10)

plt.subplot(3,3,5)
plt.plot(bcandMES,bcandDeltaE,'.',alpha=0.8,markersize=1.0)
plt.xlabel(r'M$_{\rm ES}$ [GeV/c$^{2}$]',fontsize=10)
plt.ylabel(r'$\Delta$E [GeV]',fontsize=10)

plt.tight_layout()

###################
plt.figure()
plt.subplot(3,3,1)
plt.hist(tagbcand,bins=200,range=(0,15))
plt.xlabel(r'tagB-cand mass [GeV/c$^{2}$]',fontsize=10)
    
plt.subplot(3,3,2)
plt.hist(tagbcandMES,bins=200,range=(5,5.3))
plt.xlabel(r'tagM$_{\rm ES}$ [GeV/c$^{2}$]',fontsize=10)

plt.subplot(3,3,3)
plt.hist(tagbcandDeltaE,bins=200,range=(-10,10))
plt.xlabel(r'tag$\Delta$E [GeV]',fontsize=10)

plt.subplot(3,3,4)
plt.hist(tagbcandMM,bins=200,range=(-5,7))
plt.xlabel(r'tagMissing mass [GeV/c$^{2}$]',fontsize=10)

plt.subplot(3,3,5)
plt.plot(tagbcandMES,tagbcandDeltaE,'.',alpha=0.8,markersize=1.0)
plt.xlabel(r'tagM$_{\rm ES}$ [GeV/c$^{2}$]',fontsize=10)
plt.ylabel(r'tag$\Delta$E [GeV]',fontsize=10)


plt.tight_layout()


plt.show()
