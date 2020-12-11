import numpy as np
import ROOT

import sys

import zipfile

import myPIDselector
from myPIDselector import *

#import matplotlib.pylab as plt
import pickle

eps = PIDselector("e")
pps = PIDselector("p")
pips = PIDselector("pi")
Kps = PIDselector("K")
mups = PIDselector("mu")


#particles = ["mu","e","pi","K","p"]
particle_masses = [0.000511, 0.105, 0.139, 0.494, 0.938, 0]
particle_lunds = [11, 13, 211, 321, 2212, 22]

allparts = [{}, {}, {}]

for pl in particle_lunds:
    allparts[0][pl] = []
    allparts[1][pl] = []
    allparts[2][pl] = []

################################################################################
# Read in the files and combine all the data dictionaries
################################################################################
def read_in_files_and_combine_all_the_dictionaries(infilenames,picklefile=True):
    allvars = {} # This will hold all the collected data
    histos = {}  # This initializes the necessary histogram files

    for i,infile in enumerate(infilenames):
        print("Loading " + infile)

        if picklefile:
            x = pickle.load(open(infile,'rb'))

        if i==0:
            key = list(x.keys())[0]
            ncuts = len(x[key]['values'])

            for key in x.keys():
                allvars[key] = {}
                allvars[key]['values'] = list(x[key]['values'])
                allvars[key]['xlabel'] = x[key]['xlabel']
                allvars[key]['ylabel'] = x[key]['ylabel']
                allvars[key]['range'] = x[key]['range']

                histos[key] = {}
                histos[key]['h'] = []
                histos[key]['xlabel'] = x[key]['xlabel']
                histos[key]['ylabel'] = x[key]['ylabel']
                histos[key]['range'] = x[key]['range']
        else:
            for key in x.keys():
                vals_for_all_cuts = x[key]['values']
                for i,v in enumerate(vals_for_all_cuts):
                    allvars[key]['values'][i] += v

    for key in allvars.keys():
        ncuts = len(allvars[key]['values'])
        for i in range(ncuts):
            allvars[key]['values'][i] = np.array(allvars[key]['values'][i])

    return allvars,histos


################################################################################
# Plotting utility
################################################################################
'''
def display_histogram(h,xlabel='xlabel',ylabel='ylabel',ax=None,xfontsize=12,yfontsize=12,label=None):

    if ax is not None:
        plt.sca(ax)
    
    #print(len(h[1][:-1]), len(h[0]), h[1][1]-h[1][0])
    plt.bar(h[1][:-1], h[0], width=h[1][1]-h[1][0],label=label)
    plt.gca().set_xlabel(xlabel,fontsize=xfontsize)
    plt.gca().set_ylabel(ylabel,fontsize=yfontsize)

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

################################################################################
def calc_B_variables(particles, beam, decay='pnu', momentum_cut=1.7):

    # B candidates
    bc = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    tagbc = np.array([0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0])
    highmomE = 0
    #totp4 = beam[0:4].copy()
    totp4 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    #print(totp4)

    tagq_temp = 0

    # Grab the relevant protons and leptons
    prots = []
    leps = []
    # Pmag for particles in B candidate
    protp3 = []
    lepp3 = []
    protidx = []
    lepidx = []

    tagq = []
    # Get the tag side and don't count the proton or lepton
    #print("---------")
    #print(totp4)
    for p in particles:
        #totp4 -= p[0:4]
        totp4 += p
        tagq_temp += int(p[-3])
        #print(p[-1],totp4)

        if decay=='pmu' or decay=='pe' or decay=='pnu':
            if p[-1]==2212 and vec_mag(p[1:4])>momentum_cut:
                prots.append(p)

            if decay=='pmu':
                if p[-1]==13 and vec_mag(p[1:4])>momentum_cut:
                    leps.append(p)
            elif decay=='pe':
                if p[-1]==11 and vec_mag(p[1:4])>momentum_cut:
                    leps.append(p)

        elif decay=='nmu' or decay=='ne':

            if decay=='nmu':
                if p[-1]==13 and vec_mag(p[1:4])>momentum_cut:
                    leps.append(p)
            elif decay=='ne':
                if p[-1]==11 and vec_mag(p[1:4])>momentum_cut:
                    leps.append(p)


        '''
        ##### Don't include relevant particles in the calculation of the "tag" B
        flag = True
        if decay=='pnu': # Missing neutrino, require high-mom proton
            flag = not (vec_mag(p[1:4])>momentum_cut and p[-1]==2212)
        elif decay=='nmu': # Missing neutron, require high-mom muon
            flag =  not (vec_mag(p[1:4])>momentum_cut and p[-1]==13)
        elif decay=='ne': # Missing neutron, require high-mom electron
            flag =  not (vec_mag(p[1:4])>momentum_cut and p[-1]==11)
        elif decay=='pmu': # proton+muon
            flag =  not ((vec_mag(p[1:4])>momentum_cut and p[-1]==13) or (vec_mag(p[1:4])>momentum_cut and p[-1]==2212))
        elif decay=='pe': # proton+electron
            flag =  not ((vec_mag(p[1:4])>momentum_cut and p[-1]==11) or (vec_mag(p[1:4])>momentum_cut and p[-1]==2212))

        # Old calculation (before 7/30/2020
        if flag:
            #print(p)
            tagbc += p
            tagq += p[-2]
        else:
            highmomE += p[0]
            #print(p[-1],vec_mag(p[1:]))
        '''

        '''
        # New calculation (7/30/2020
        # Include everything in the tag! 
        # We'll subtract out the other stuff later!
        ##### Don't include relevant particles in the calculation of the "tag" B
        # Flag now means something different than before
        flag = True
        if decay=='pnu': # Missing neutrino, require high-mom proton
            flag = vec_mag(p[1:4])>momentum_cut and p[-1]==2212
        elif decay=='nmu': # Missing neutron, require high-mom muon
            flag =  vec_mag(p[1:4])>momentum_cut and p[-1]==13
        elif decay=='ne': # Missing neutron, require high-mom electron
            flag =  vec_mag(p[1:4])>momentum_cut and p[-1]==11
        elif decay=='pmu': # proton+muon
            flag =  (vec_mag(p[1:4])>momentum_cut and p[-1]==13) or (vec_mag(p[1:4])>momentum_cut and p[-1]==2212)
        elif decay=='pe': # proton+electron
            flag =  (vec_mag(p[1:4])>momentum_cut and p[-1]==11) or (vec_mag(p[1:4])>momentum_cut and p[-1]==2212)
        
        # Add everything into the tag and we'll subtract it out later
        tagbc += p
        tagq_temp += int(p[-3])
        # If it's not
        if flag:
            highmomE += p[0]
            #print(p[-1],vec_mag(p[1:]))
        '''


    halfbeam = beam[0]/2.0
    #print(halfbeam)

    #print(totp4)
    missingp4 = beam - totp4
    missingmom = vec_mag(missingp4[1:4])
    missingE = missingp4[0]

    # For later calculations we want to set the missingp4 energy
    # to be 0. 
    missingp4[0] = 0.0

    ######################################################
    # See if we have any BNV B candidates
    ######################################################
    bcands_temp = []
    tagcands_temp = []
    bcand = []
    dE = []
    mes = []
    tagbcand = []
    tagdE = []
    tagmes = []
    missingmass = []
    if decay=='nmu' or decay=='ne':
        #if len(prots)==0:
        #prots = [np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])]
        prots = [missingp4]
    if decay=='pnu':
        #if len(leps)==0:
            #leps = [np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])]
        leps = [missingp4]
    #if decay=='pmu' or decay=='pe':
    #print("--------")
    #print(prots)
    #print(leps)
    if 1:
        for p0 in prots:
            #print('----')
            for l0 in leps:
                #print(p0)
                #print(l0)
                # Check the charge
                #print("Tot charge: ", p0[-3]*l0[-3])
                if p0[-3]*l0[-3]<=0:
                    #print('FOUND BCAND!')
                    bcp4 = p0+l0
                    #print("here!!!!!!!!!")
                    #print(bcp4)
                    #bcands_temp.append(p0+l0)
                    bcands_temp.append(bcp4)
                    protp3.append(vec_mag(p0[1:4]))
                    protidx.append(p0[-2])
                    #print(l0)
                    lepp3.append(vec_mag(l0[1:4]))
                    lepidx.append(l0[-2])

                    # Recalculate the missing mass assuming B on one side
                    #totp4[0] = halfbeam - highmomE
                    #missingmass = invmass([totp4],return_squared=True)
                    totp4_temp = missingp4
                    # Try to improve the resolution by replacing some of the 
                    # B beam energy with 1/2 the beam
                    #totp4_temp[0] = halfbeam - bcp4[0]
                    # Need to not use the combined p4 for the calculation of missing energies
                    if decay=='pmu' or decay=='pe':
                        totp4_temp[0] = beam[0] - (halfbeam + bcp4[0])
                    elif decay=='pnu':
                        totp4_temp[0] = beam[0] - (halfbeam + p0[0])
                    elif decay=='nmu' or decay=='ne':
                        totp4_temp[0] = beam[0] - (halfbeam + l0[0])
                    m = invmass([totp4_temp],return_squared=True)
                    #print(totp4_temp)
                    #print(m,halfbeam,bcp4[0])
                    missingmass.append(m)

                    #for bc in bcands_temp:
                    bcand.append(invmass([bcp4]))
                    dE.append(bcp4[0] - halfbeam)
                    # Save this for use with the tag side
                    bcp4E_org = bcp4[0]
                    bcp4[0] = halfbeam
                    mes.append(invmass([bcp4]))

                    #print("----------------")
                    #print(tagbc)
                    #print(bcp4)
                    #print(tagbc-bcp4)
                    #print(invmass([tagbc-bcp4]))

                    tagbp4 = None
                    if decay=='pmu' or decay=='pe':
                        tagbp4 = totp4 - bcp4 
                    elif decay=='pnu':
                        tagbp4 = totp4 - p0
                    elif decay=='nmu' or decay=='ne':
                        tagbp4 = totp4 - l0 

                    #tagbcand.append(invmass([tagbc-bcp4]))
                    tagbcand.append(invmass([tagbp4]))
                    #tagdE.append(tagbc[0] - halfbeam)
                    # Need to use the original bcp4 because we modified it.
                    tagdE.append(totp4[0] - bcp4E_org - halfbeam)

                    #tagbc_temp = tagbc - bcp4
                    tagbp4[0] = halfbeam
                    tagmes.append(invmass([tagbp4]))

                    tagq.append(tagq_temp - int(p0[-3]) - int(l0[-3]))
                    #totp4[0] = halfbeam
                    #tagmes = invmass([tagbc])

    #print(lepp3)
    nbnvbcand = len(bcands_temp)
    #if len(bcands_temp)==1:
        #bc = bcands_temp[0]

    ########################################################
    # Recalculate the missing mass assuming B on one side
    #totp4[0] = halfbeam - highmomE
    #missingmass = invmass([totp4],return_squared=True)

    #print(beam)
    #print(halfbeam)

    '''
    bcand = []
    dE = []
    mes = []
    for bc in bcands_temp:
        bcand.append(invmass([bc]))
        dE.append(bc[0] - halfbeam)
        bc[0] = halfbeam
        mes.append(invmass([bc]))

    tagbcand = invmass([tagbc])
    tagdE = tagbc[0] - halfbeam
    tagbc[0] = halfbeam
    tagmes = invmass([tagbc])
    '''

    return nbnvbcand,bcand,dE,mes,protp3,lepp3,protidx,lepidx, tagbcand,tagdE,tagmes, tagq, missingmom, missingE, missingmass


