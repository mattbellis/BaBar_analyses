import numpy as np
import matplotlib.pylab as plt

import ROOT

import sys
import os

import lichen.lichen as lch

from myPIDselector import *

import pickle

from babar_tools import vec_mag,angle,selectPID,invmass,recalc_energy,sph2cart
from babar_tools import particle_masses,particle_lunds
from babar_tools import eps,pps,pips,Kps,mups # The PID selectors for each particle

#plt.switch_backend('Agg')

#eps = PIDselector("e")
#pps = PIDselector("p")
#pips = PIDselector("pi")
#Kps = PIDselector("K")
#mups = PIDselector("mu")



#particles = ["mu","e","pi","K","p"]
#particle_masses = [0.000511, 0.105, 0.139, 0.494, 0.938, 0]
#particle_lunds = [11, 13, 211, 321, 2212, 22]

plotvars = {}
plotvars["bcandmass"] = {"values":[], "xlabel":r"Mass B-candidate [GeV/c$^{2}$]", "ylabel":r"# entries","range":(0,6)} 
plotvars["bcandMES"] = {"values":[], "xlabel":r"M$_{\rm ES}$ [GeV/c$^{2}$]", "ylabel":r"# entries","range":(5.2,5.3)} 
plotvars["bcandDeltaE"] = {"values":[], "xlabel":r"$\Delta E$ [GeV]", "ylabel":r"# entries","range":(-2,2)} 
plotvars["pmom"] = {"values":[], "xlabel":r"proton $|p|$ [GeV/c]", "ylabel":r"# entries","range":(0,5.5)} 
plotvars["lepmom"] = {"values":[], "xlabel":r"lepton $|p|$ [GeV/c]", "ylabel":r"# entries","range":(0,5.5)} 
plotvars["r2"] = {"values":[], "xlabel":r"R2", "ylabel":r"# entries","range":(0,1)} 
plotvars["r2all"] = {"values":[], "xlabel":r"R2 all", "ylabel":r"# entries","range":(0,1)} 
plotvars["thrustmag"] = {"values":[], "xlabel":r"Thrust mag", "ylabel":r"# entries","range":(0,1)} 
plotvars["thrustmagall"] = {"values":[], "xlabel":r"Thrust mag all", "ylabel":r"# entries","range":(0,1)} 
plotvars["thrustcosth"] = {"values":[], "xlabel":r"Thrust $\cos(\theta)$", "ylabel":r"# entries","range":(-1,1)} 
plotvars["thrustcosthall"] = {"values":[], "xlabel":r"Thrust $\cos(\theta)$ all", "ylabel":r"# entries","range":(-1,1)} 
plotvars["sphericityall"] = {"values":[], "xlabel":r"Sphericity all", "ylabel":r"# entries","range":(0,1)} 
plotvars["ncharged"] = {"values":[], "xlabel":r"# charged particles", "ylabel":r"# entries","range":(0,20)} 
plotvars["nphot"] = {"values":[], "xlabel":r"# photons","ylabel":r"# entries","range":(0,20)} 

cuts = []
ncuts = 7
for n in range(ncuts):
    for key in plotvars.keys():
        plotvars[key]["values"].append([])

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

tree = ROOT.TChain("Tskim")
for i,infile in enumerate(infilenames):
    print(infile)
    tree.AddFile(infile)
    
    '''
    if i>100:
        break
    '''

nentries = tree.GetEntries()
print(nentries)
exit()

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
        tag = name.split('basicPID_R24-SP-')[1].split('-R24-')[0]
    return tag
################################################################################

outfilename = None
sptag = None
if outfilename is None:
    sptag = get_sptag(infilenames[0]) 
    outfilename = 'OUTPUT_' + lepton_to_study + '_' + sptag + ".pkl"
    #outfilename = 'OUTPUT_MUON_' + sptag + ".pkl"
    #outfilename = 'OUTPUT_ELECTRON_' + sptag + ".pkl"
    #outfilename = "output_testing_the_PID_assignment_skim.pkl"


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
    #print(beammass)
    r2 = tree.r2
    r2all = tree.r2all
    thrustmag = tree.thrustmag
    thrustmagall = tree.thrustmagall
    thrustcosth = tree.thrustcosth
    thrustcosthall = tree.thrustcosthall
    sphericityall = tree.sphericityall
        
    nphot = tree.ngamma
    ncharged = tree.npi + tree.nk + tree.nproton + tree.ne + tree.nmu

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
    #print(tree.nproton,tree.ne,tree.nmu,sum(tree.protonq),sum(tree.eq),sum(tree.muq))
    for iprot in range(tree.nproton):
        pbits = []
        pbits.append(tree.protonpibit[iprot])
        pbits.append(tree.protonkbit[iprot])
        pbits.append(tree.protonpbit[iprot])
        pbits.append(tree.protonebit[iprot])
        pbits.append(tree.protonmubit[iprot])
        # ELECTRON MUON
        counter = tree.nmu
        if lepton_to_study == 'ELECTRON':
            counter = tree.ne
        #for ilep in range(tree.ne):
        #for ilep in range(tree.nmu):
        for ilep in range(counter):

            proton = np.array([tree.protone[iprot],tree.protonpx[iprot],tree.protonpy[iprot],tree.protonpz[iprot],tree.protonq[iprot]])
            #new_energy = recalc_energy(0.938272,[proton[1],proton[2],proton[3]])
            #proton[0] = new_energy
            
            lepton = None
            lepbits = []
            if lepton_to_study == 'ELECTRON':
                # ELECTRON
                lepton = np.array([tree.ee[ilep],tree.epx[ilep],tree.epy[ilep],tree.epz[ilep],tree.eq[ilep]])
                lepbits.append(tree.epibit[ilep])
                lepbits.append(tree.ekbit[ilep])
                lepbits.append(tree.epbit[ilep])
                lepbits.append(tree.eebit[ilep])
                lepbits.append(tree.emubit[ilep])
            else:
                # MUON
                lepton = [tree.mue[ilep],tree.mupx[ilep],tree.mupy[ilep],tree.mupz[ilep],tree.muq[ilep]]
                lepbits.append(tree.mupibit[ilep])
                lepbits.append(tree.mukbit[ilep])
                lepbits.append(tree.mupbit[ilep])
                lepbits.append(tree.muebit[ilep])
                lepbits.append(tree.mumubit[ilep])

            #print("hi")
            #print(proton)
            #print(lepton)

            # Make sure the charges are not the same
            if proton[4] == lepton[4]:
                continue

            pp = vec_mag(proton[1:4])
            lp = vec_mag(lepton[1:4])

            bc = proton[0:-1] + lepton[0:-1]
            bc_mass = invmass([bc])

            dE = bc[0] - beam[0]/2.0
            bc[0] = beam[0]/2.0
            mes = invmass([bc])

            pidx = proton[-1]
            lidx = lepton[-1]
            
            # Should the low cut be 2.2 or 2.3? 
            cut1 = pp>2.3 and pp<2.8 and lp>2.3 and lp<2.8
            cut2 = dE>-0.5
            cut3 = r2all<0.5
            cut4 = ncharged>5

            pps.SetBits(pbits[2]); 
            cut5 = pps.IsSelectorSet("SuperTightKMProtonSelection")

            if lepton_to_study == 'ELECTRON':
                # ELECTRON
                eps.SetBits(lepbits[3]); 
                cut5 *= eps.IsSelectorSet("SuperTightKMElectronMicroSelection")
                cut6 = (tree.nproton%2==1 or (tree.nproton==2 and sum(tree.protonq)!=0)) and (tree.ne%2==1 or (tree.ne==2 and sum(tree.eq)!=0))
            else:
                # MUON
                mups.SetBits(lepbits[4]); 
                cut5 *= mups.IsSelectorSet("BDTVeryTightMuonSelectionFakeRate") or mups.IsSelectorSet("BDTVeryTightMuonSelection") 
                cut6 = (tree.nproton%2==1 or (tree.nproton==2 and sum(tree.protonq)!=0)) and (tree.nmu%2==1 or (tree.nmu==2 and sum(tree.muq)!=0))

            cuts = [1, cut1, (cut2*cut1), (cut1*cut2*cut3), (cut1*cut2*cut3*cut4), (cut1*cut2*cut3*cut4*cut5), (cut1*cut2*cut3*cut4*cut5*cut6)]
            for icut,cut in enumerate(cuts):
                if cut:
                    #print(icut)
                    plotvars["bcandmass"]["values"][icut].append(bc_mass)

                    plotvars["bcandMES"]["values"][icut].append(mes)
                    plotvars["bcandDeltaE"]["values"][icut].append(dE)

                    plotvars["pmom"]["values"][icut].append(pp)
                    plotvars["lepmom"]["values"][icut].append(lp)

                    plotvars["r2"]["values"][icut].append(r2)
                    plotvars["r2all"]["values"][icut].append(r2all)
                    plotvars["thrustmag"]["values"][icut].append(thrustmag)
                    plotvars["thrustmagall"]["values"][icut].append(thrustmagall)
                    plotvars["thrustcosth"]["values"][icut].append(thrustcosth)
                    plotvars["thrustcosthall"]["values"][icut].append(thrustcosthall)
                    plotvars["sphericityall"]["values"][icut].append(sphericityall)

                    plotvars["nphot"]["values"][icut].append(nphot)
                    plotvars["ncharged"]["values"][icut].append(ncharged)


                    '''
                    if icut==5 and mes>5.2:
                        print("-----------------------------")
                        print("   --- LEPTON ")
                        print(lepbits)
                        print("pi"); pips.SetBits(lepbits[0]); pips.PrintSelectors(); #Kps.PrintBits()
                        print("K "); Kps.SetBits(lepbits[1]); Kps.PrintSelectors(); #Kps.PrintBits()
                        print("p "); pps.SetBits(lepbits[2]); pps.PrintSelectors(); #Kps.PrintBits()
                        print("e"); eps.SetBits(lepbits[3]); eps.PrintSelectors(); #Kps.PrintBits()
                        print("mu"); mups.SetBits(lepbits[4]); mups.PrintSelectors(); #Kps.PrintBits()

                        print("\n   --- PROTON ")
                        print(pbits)
                        print("pi"); pips.SetBits(pbits[0]); pips.PrintSelectors(); #Kps.PrintBits()
                        print("K "); Kps.SetBits(pbits[1]); Kps.PrintSelectors(); #Kps.PrintBits()
                        print("p "); pps.SetBits(pbits[2]); pps.PrintSelectors(); #Kps.PrintBits()
                        print("e"); eps.SetBits(pbits[3]); eps.PrintSelectors(); #Kps.PrintBits()
                        print("mu"); mups.SetBits(pbits[4]); mups.PrintSelectors(); #Kps.PrintBits()
                    '''

            #bcandMM.append(invmass([beam-bc]))

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

#exit()

outfile = open(outfilename,'wb')
pickle.dump(plotvars,outfile)
outfile.close()

print('Processed {0} files for {1}'.format(len(infilenames),sptag))

exit()

#print(bcand)
for icut,cut in enumerate(cuts):
    for j,key in enumerate(plotvars.keys()):
        var = plotvars[key]
        print(len(var["values"][icut])/nentries)
#exit()


for icut,cut in enumerate(cuts):
    plt.figure(figsize=(10,6))
    for j,key in enumerate(plotvars.keys()):
        var = plotvars[key]
        plt.subplot(4,4,1+j)
        if key=="nphot" or key=="ncharged":
            lch.hist_err(var["values"][icut],range=var["range"],bins=20,alpha=0.2,markersize=0.5)
        else:
            lch.hist_err(var["values"][icut],range=var["range"],bins=50,alpha=0.2,markersize=0.5)
        plt.xlabel(var["xlabel"],fontsize=12)
        plt.ylabel(var["ylabel"],fontsize=12)
        print(len(var["values"][icut]))

    if icut==len(cuts)-1:
        plt.figure(figsize=(10,6))
        plt.subplot(1,1,1)
        plt.plot(plotvars["bcandMES"]["values"][icut],plotvars["bcandDeltaE"]["values"][icut],'.',alpha=0.8,markersize=2.0)
        plt.xlabel(plotvars["bcandMES"]["xlabel"],fontsize=12)
        plt.ylabel(plotvars["bcandMES"]["ylabel"],fontsize=12)
        plt.xlim(5.2,5.3)
        plt.ylim(-0.4,0.1)


        plt.tight_layout()
    plt.tight_layout()

plt.show()
