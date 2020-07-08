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
def calc_B_variables(particles, beam, decay='pnu'):

    # B candidates
    bc = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    tagbc = np.array([0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0])
    highmomE = 0
    totp4 = beam[0:4].copy()
    #print(totp4)


    tagq = 0

    # Grab the relevant protons and leptons
    prots = []
    leps = []
    # Pmag for particles in B candidate
    protp3 = []
    lepp3 = []
    protidx = []
    lepidx = []
    # Get the tag side and don't count the proton or lepton
    #print("---------")
    #print(totp4)
    for p in particles:
        totp4 -= p[0:4]
        #print(p[-1],totp4)

        if decay=='pmu' or decay=='pe':
            if p[-1]==2212 and vec_mag(p[1:4])>2.0:
                prots.append(p)

            if decay=='pmu':
                if p[-1]==13 and vec_mag(p[1:4])>2.0:
                    leps.append(p)
            elif decay=='pe':
                if p[-1]==11 and vec_mag(p[1:4])>2.0:
                    leps.append(p)


        ##### Don't include relevant particles in the calculation of the "tag" B
        flag = True
        if decay=='pnu': # Missing neutrino, require high-mom proton
            flag = not (vec_mag(p[1:4])>2.0 and p[-1]==2212)
        elif decay=='nmu': # Missing neutron, require high-mom muon
            flag =  not (vec_mag(p[1:4])>2.0 and p[-1]==13)
        elif decay=='ne': # Missing neutron, require high-mom electron
            flag =  not (vec_mag(p[1:4])>2.0 and p[-1]==11)
        elif decay=='pmu': # proton+muon
            flag =  not ((vec_mag(p[1:4])>2.0 and p[-1]==13) or (vec_mag(p[1:4])>2.0 and p[-1]==2212))
        elif decay=='pe': # proton+electron
            flag =  not ((vec_mag(p[1:4])>2.0 and p[-1]==11) or (vec_mag(p[1:4])>2.0 and p[-1]==2212))

        if flag:
            #print(p)
            tagbc += p
            tagq += p[-2]
        else:
            highmomE += p[0]
            #print(p[-1],vec_mag(p[1:]))

    ######################################################
    # See if we have any BNV B candidates
    ######################################################
    bcands_temp = []
    if decay=='pmu' or decay=='pe':
        for p0 in prots:
            for l0 in leps:
                if p0[-2]*l0[-2]<0:
                    bcands_temp.append(p0+l0)
                    protp3.append(vec_mag(p0[1:4]))
                    protidx.append(p0[-2])
                    #print(l0)
                    lepp3.append(vec_mag(l0[1:4]))
                    lepidx.append(l0[idx])

    #print(lepp3)
    nbnvbcand = len(bcands_temp)
    #if len(bcands_temp)==1:
        #bc = bcands_temp[0]

    ########################################################
    halfbeam = beam[0]/2.0
    #print(halfbeam)

    #print(totp4)
    missingmom = vec_mag(totp4[1:])
    missingE = totp4[0]

    # Recalculate the missing mass assuming B on one side
    totp4[0] = halfbeam - highmomE
    missingmass = invmass([totp4],return_squared=True)

    #print(beam)
    #print(halfbeam)

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

    return nbnvbcand,bcand,dE,mes,protp3,lepp3,protidx,lepidx, tagbcand,tagdE,tagmes, tagq, missingmom, missingE, missingmass


################################################################################
def return_dataset_information(verbose=False):
    # Information about BaBar detector and luminosity
    # https://www.sciencedirect.com/science/article/pii/S0168900213007183
    raw_event_numbers = {}
    raw_event_numbers["DATA"] = {}
    raw_event_numbers["MC"] = {}
    
    for i in range(1,7):
            key = "Run{0}".format(i)
            raw_event_numbers["DATA"][key] = {"raw":1, "xsec":0}
    
    for i in [1235, 1237, 1005, 998, 3429, 3981, 2400, 11975, 11976, 11977, 9456, 9457, 980]:
            key = "{0}".format(i)
            raw_event_numbers["MC"][key] = {"raw":1, "xsec":1}
    
    #raw_event_numbers["DATA"]["Run1"]["raw"] *= 2929
    #raw_event_numbers["DATA"]["Run2"]["raw"] *= 9590
    #raw_event_numbers["DATA"]["Run3"]["raw"] *= 5014
    #raw_event_numbers["DATA"]["Run4"]["raw"] *= 15936
    #raw_event_numbers["DATA"]["Run5"]["raw"] *= 21045
    #raw_event_numbers["DATA"]["Run6"]["raw"] *= 12629
    raw_event_numbers["DATA"]["Run1"]["raw"] = 292782011
    raw_event_numbers["DATA"]["Run2"]["raw"] = 958854016
    raw_event_numbers["DATA"]["Run3"]["raw"] = 501277316
    raw_event_numbers["DATA"]["Run4"]["raw"] = 1593488357
    raw_event_numbers["DATA"]["Run5"]["raw"] = 2104338820
    raw_event_numbers["DATA"]["Run6"]["raw"] = 1262797446
    
    raw_event_numbers["MC"]["1235"]["raw"] = 710352000
    raw_event_numbers["MC"]["1237"]["raw"] = 719931000
    raw_event_numbers["MC"]["1005"]["raw"] = 1133638000
    raw_event_numbers["MC"]["998"]["raw"] = 3595740000
    raw_event_numbers["MC"]["3429"]["raw"] = 1620027000
    raw_event_numbers["MC"]["3981"]["raw"] = 622255000
    raw_event_numbers["MC"]["2400"]["raw"] = 472763000
    
    raw_event_numbers["MC"]["980"]["raw"] = 2149000
    
    raw_event_numbers["MC"]["9456"]["raw"] = 4298000
    raw_event_numbers["MC"]["9457"]["raw"] = 4298000
    raw_event_numbers["MC"]["11975"]["raw"] = 4514000
    raw_event_numbers["MC"]["11976"]["raw"] = 4494000
    raw_event_numbers["MC"]["11977"]["raw"] = 4514000
    
    raw_event_numbers["MC"]["1235"]["xsec"] = 0.54
    raw_event_numbers["MC"]["1237"]["xsec"] = 0.54
    raw_event_numbers["MC"]["1005"]["xsec"] = 1.30
    raw_event_numbers["MC"]["998"]["xsec"] = 2.09
    raw_event_numbers["MC"]["3429"]["xsec"] = 0.94
    raw_event_numbers["MC"]["3981"]["xsec"] = 1.16
    raw_event_numbers["MC"]["2400"]["xsec"] = 40
    
    intlumi = 424.18
    
    
    # Section 6.2 of above paper
    # The final dataset contains more than nine billion events passing the pre-reconstruction filter described above, primarily taken on the  resonance. 
    
    
    tot = 0
    for key in raw_event_numbers["DATA"].keys():
        tot += raw_event_numbers["DATA"][key]["raw"]
    
    if verbose:
        print(tot,tot/1e9)
    
    bkg = [1235, 1237, 1005, 998, 3429, 3981, 2400]
    tot = 0
    for sp in bkg:
        key = "{0}".format(sp)
        xsec = raw_event_numbers["MC"][key]["xsec"]
        raw = raw_event_numbers["MC"][key]["raw"]
        weight = (raw/1e6)/(xsec*intlumi)
        raw_event_numbers["MC"][key]["scale_factor"] = weight
        raw_event_numbers["MC"][key]["weight"] = 1.0/weight

        if verbose:
            print("{0:4s} {1:4.2f} {2:-9.2f} {3:6.2f} {4:6.2f}".format(key, xsec, xsec*intlumi, raw/1e6, (raw/1e6)/(xsec*intlumi)))
        tot += xsec
    if verbose:
        print(tot)

    return raw_event_numbers
    
################################################################################
def get_sptag(name):

    labels = {}
    labels['1235'] = r'$B^+B^-$'
    labels['1237'] = r'$B^0\bar{B}^0$'
    labels['1005'] = r'$c\bar{c}$'
    labels['998'] = r'$u\bar{u},d\bar{d},s\bar{s}$'
    labels['3429'] = r'$\tau^+\tau^-$'
    labels['3981'] = r'$\mu^+\mu^-$'
    labels['signal'] = r'$B\rightarrow p \ell^-$'

    tag = None
    label = None
    if name.find('AllEvents')>=0:
        # Data
        # basicPID_R24-AllEvents-Run1-OnPeak-R24-9_SKIMMED.root
        tag = name.split('basicPID_R24-AllEvents-')[1].split('-OnPeak-R24-')[0]
        label = 'Data'
    elif name.find('SP')>=0:
        # MC
        index = name.find('SP')+1
        sps = ['1235', '1237', '1005', '998', '3429', '3981']
        for sp in sps:
            if name.find(sp,index)>=index:
                break
        tag = sp
        label = labels[sp]
    return tag,label
################################################################################
