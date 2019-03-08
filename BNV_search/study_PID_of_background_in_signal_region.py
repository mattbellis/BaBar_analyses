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

#filenames = sys.argv[1:]
outfilename = None
if outfilename is None:
    #outfilename = filenames[0].split('/')[-1].split('.root')[0] + "_OUTPUT.root"
    outfilename = "testing_the_skim_output.root"
outfile = ROOT.TFile(outfilename, "RECREATE")
outfile.cd()

outtree = ROOT.TTree("Tskim", "Our tree of everything")

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

nentries = 1000


for i in range(nentries):

    #myparticles = {"electrons":[], "muons":[], "pions":[], "kaons":[], "protons":[], "gammas":[]}
    #myparticles = [[], [], [], [], [], []]
    myparticles = []


    if i%1000==0:
        print(i,nentries)

    if i>100000000:
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
    npi[0] = 0
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

        if lund==211:
            pie[npi[0]] = e
            pipx[npi[0]] = px
            pipy[npi[0]] = py
            pipz[npi[0]] = pz
            piq[npi[0]] = q

            npi[0] += 1

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

    outtree.Fill()

outfile.cd()
outfile.Write()
outfile.Close()



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
