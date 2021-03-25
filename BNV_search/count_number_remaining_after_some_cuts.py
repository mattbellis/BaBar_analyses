import numpy as np
import sys
import pandas as pd

import plotting_tools as pt
import babar_dataframe_tools as bd

infilenames = sys.argv[1:]

counts = {}
decays = ['pmu', 'pe', 'pnu', 'nmu', 'ne']
for decay in decays:
    counts[decay] = {}


#tag = 'tighterPID_childmomentum'
#tag = 'selection_cuts'
tag = 'selection_cuts_TESTING'
for infilename in infilenames:

    print(infilename)

    sp = pt.get_sptag(infilename)

    decays = ['pmu', 'pe', 'pnu', 'nmu', 'ne']
    for d in decays:
        if infilename.find('_'+d)>=0:
            decay = d
            break
        
    #print(decay,sp)

    df = pd.read_hdf(infilename)
    cut0 = len(df)

    if decay=='pmu':
        pid_mask0 = bd.pid_mask(df,particle='proton')
        pid_mask1 = bd.pid_mask(df,particle='muon')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='muon')
        bnv_children_costh_mask = bd.bnv_children_costh_mask(df,child='proton') & bd.bnv_children_costh_mask(df,child='muon')
    elif decay=='pe':
        pid_mask0 = bd.pid_mask(df,particle='proton')
        pid_mask1 = bd.pid_mask(df,particle='electron')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='electron')
        bnv_children_costh_mask = bd.bnv_children_costh_mask(df,child='proton') & bd.bnv_children_costh_mask(df,child='electron')
    elif decay=='pnu':
        pid_mask0 = bd.pid_mask(df,particle='proton')
        pid_mask1 = bd.pid_mask(df,particle='proton')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='nu')
        bnv_children_costh_mask = bd.bnv_children_costh_mask(df,child='proton') 
    elif decay=='nmu':
        pid_mask0 = bd.pid_mask(df,particle='muon')
        pid_mask1 = bd.pid_mask(df,particle='muon')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='neutron') & bd.bnv_children_momentum_mask(df,child='muon')
        bnv_children_costh_mask = bd.bnv_children_costh_mask(df,child='muon')
    elif decay=='ne':
        pid_mask0 = bd.pid_mask(df,particle='electron')
        pid_mask1 = bd.pid_mask(df,particle='electron')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='neutron') & bd.bnv_children_momentum_mask(df,child='electron')
        bnv_children_costh_mask = bd.bnv_children_costh_mask(df,child='electron')



    #cut1 = len(df[pid_mask0])
    #cut2 = len(df[pid_mask1])
    #cut3 = len(df[pid_mask0 & pid_mask1])
    #cut4 = len(df[bnv_children_momentum_mask])
    #cut5 = len(df[pid_mask0 & pid_mask1 & bnv_children_momentum_mask])

    dsc_mask = bd.decay_specific_cuts(df,decay=decay)

    cut1 = len(df[pid_mask0])
    cut2 = len(df[pid_mask0 & pid_mask1])
    cut3 = len(df[pid_mask0 & pid_mask1 & bnv_children_momentum_mask])
    cut4 = len(df[pid_mask0 & pid_mask1 & bnv_children_momentum_mask & bnv_children_costh_mask])
    cut5 = len(df[dsc_mask])

    if sp[0] in list(counts[decay].keys()):
        #counts[decay][sp[0]] += cut5
        counts[decay][sp[0]] += cut4
    else:
        #counts[decay][sp[0]] = cut5
        counts[decay][sp[0]] = cut4
    #counts[decay][sp[0]] = cut5

    print(cut0,cut1,cut2,cut3,cut4,cut5)
    if cut0>0:
        print(f"Org: {cut0/cut0:.6f} PID1: {cut1/cut0:.6f} PID_BOTH: {cut2/cut0:.6f} PIDBoth+BNVmom: {cut3/cut0:.6f} PIDBoth+BNVmom+costh: {cut4/cut0:.6f} SELCUTS: {cut5/cut0:.6f}")

    #exit()

output = ""
for decay in decays:
    output += "# {0}\n".format(decay)
    for sp in counts[decay].keys():

        datatype = 'MC'
        if sp.find('Run')>=0 or sp.find('All')>=0:
            datatype = 'DATA'

        num = counts[decay][sp]

        output += 'event_numbers["{3}"]["{0}"]["{1}"]["{4}"] = {2:d}\n'.format(decay,sp,num,datatype,tag)
        ##print(decay,sp,)
print(output)

outfile = open(f"COUNTS_TEST_{tag}.py",'w')
outfile.write(output)
outfile.close()
