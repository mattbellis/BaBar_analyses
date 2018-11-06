import numpy as np
import matplotlib.pylab as plt

import ROOT

import sys

#import lichen.lichen as lch

plt.switch_backend('Agg')

#particles = ["mu","e","pi","K","p"]
particle_masses = [0.000511, 0.105, 0.139, 0.494, 0.938, 0]
particle_lunds = [11, 13, 211, 321, 2212, 22]

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

tree = ROOT.TChain("Tskim")
for infile in sys.argv[1:]:
    print(infile)
    tree.AddFile(infile)

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
    outfilename = "output_testing_the_PID_assignment_skim.root"
outfile = ROOT.TFile(outfilename, "RECREATE")
outfile.cd()

#outtree = ROOT.TTree("Tskim", "Our tree of everything")

for i in range(nentries):

    if i%1000==0:
        print(i,nentries)

    if i>100000000:
        break

    tree.GetEntry(i)

    nvals = 0

    #beam = np.array([tree.eeE, tree.eePx, tree.eePy, tree.eePz, 0, 0])
    beamp4 = np.array([tree.beame, tree.beampx, tree.beampy, tree.beampz])
    beammass = invmass([beamp4])
    beam = np.array([beammass, 0.0, 0.0, 0.0, 0, 0])

        
    '''
    if particle[-1]==11 and pmag>2.25 and pmag<2.8:
        leptons.append(np.array(particle + [j]))
    elif particle[-1]==2212 and pmag>2.25 and pmag<2.8:
        protons.append(np.array(particle + [j]))
    '''
    #exit()

    ############################################################################
    # Print out the photons
    ############################################################################
    '''
    for electron in leptons:
        ang = angle(electron[1:4],particle[1:4])#,returncos=True)
        angles.append(ang)

        # Add Brehm photons
        # WHAT IF PHOTON IS CLOSE TO TWO OR MORE leptons????
        #if ang>=0.9958: # Do this for cos
        #if ang<=0.20:
        if ang<=0.05:
            #print(electron)
            electron[0:4] += particle[0:4]
            #print(electron)
        else:
            myparticles.append(particle)
    '''

    nbcand = 0
    for iprot in range(tree.nproton):
        for ilep in range(tree.ne):

            proton = [tree.protone[iprot],tree.protonpz[iprot],tree.protonpy[iprot],tree.protonpz[iprot],tree.protonq[iprot]]
            lepton = [tree.ee[iprot],tree.epz[iprot],tree.epy[iprot],tree.epz[iprot],tree.eq[iprot]]

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
            
            bcand.append(invmass([bc]))
            dE = bc[0] - beam[0]/2.0
            bc[0] = beam[0]/2.0
            mes = invmass([bc])
            bcandMES.append(mes)
            bcandDeltaE.append(dE)
            bcandMM.append(invmass([beam-bc]))

            #tagbcand.append(invmass([tagbc]))
            #tagdE = tagbc[0] - beam[0]/2.0
            #tagbc[0] = beam[0]/2.0
            #tagmes = invmass([tagbc])
            #tagbcandMES.append(tagmes)
            #tagbcandDeltaE.append(tagdE)
            #tagbcandMM.append(invmass([beam-tagbc]))

            nbcand += 1
        
    #totqs.append(totq)
    nbcands.append(nbcand)

    #outtree.Fill()

#outfile.cd()
#outfile.Write()
#outfile.Close()

