import numpy as np
import matplotlib.pylab as plt

import sys

from raw_event_numbers_and_cross_section import raw_event_numbers
from selection_numbers import event_numbers as skim_numbers
from selection_numbers_after_cuts1 import event_numbers as cuts1_numbers
#from selection_numbers_after_cuts2 import event_numbers as cuts2_numbers
from COUNTS_TEST_selection_cuts import event_numbers as cuts2_numbers
from plotting_tools import get_sptag

#outMC = open("CUTS_SUMMARY_MC.tex",'w')
#outDATA = open("CUTS_SUMMARY_DATA.tex",'w')

outMC = open("CUTS_SUMMARY_MC_CUTS2.tex",'w')
outDATA = open("CUTS_SUMMARY_DATA_CUTS2.tex",'w')

datatypes = ['DATA','MC']
decays = ['pmu', 'pe', 'pnu', 'nmu', 'ne']
sps = ['9456', '9457', '11975', '11976', '11977' ,'1235', '1237', '1005', '998']#, '2400', '3981', '3429']
runs = ['Run1', 'Run2', 'Run3', 'Run4', 'Run5', 'Run6']

################################################################################
#'''
for decay in decays:
    output = '\\begin{table}\n'
    #output += '\\caption{Cuts flow for MC for ' +decay + ' final state. Cuts are described in the text.\\label{tab:cutflow' +decay+ '}}\n'
    output += '\\caption{Cuts flow for MC for ' +decay + ' final state. Cuts are described in the text.\\label{tab:cutflow2' +decay+ '}}\n'
    output += '\\begin{tabular}{l l r | r r | r r}\n'
    #output += '\\multicolumn{7}{c}{' + decay + '}\\\\\n'
    # CUTS 1
    #output += 'SP & & Raw events & Skim events & Skim \% & Cuts events & Cuts \% of raw \\\\\n'
    # CUTS 2
    output += 'SP & & Raw events & Previous cuts & Cuts step 2 & Cuts frac. of prev & Cuts frac. of raw \\\\\n'
    output += '\\hline\n'
    for sp in sps:
        sptag = get_sptag('SP'+sp)
        raw = raw_event_numbers['MC'][sp]['raw']
        skim = skim_numbers['MC'][sp]['skim']
        cuts1 = cuts1_numbers['MC'][decay][sp]['cuts1']
        #cuts2 = cuts2_numbers['MC'][decay][sp]['tighterPID_childmomentum']
        cuts2 = cuts2_numbers['MC'][decay][sp]['selection_cuts']

        if sp=='1235':
            output += '\\hline\n'

        #print('{0:3} {1:5} {2:10d} {3:8.3e} {4:8.3e}'.format( decay, sp, raw, skim/raw, cuts1/raw))
        # CUTS 1
        #output += '{0:5} & {1:12} & {2:10d} & {3:10d} & {4:6.2e} & {5:10d} & {6:6.2e} \\\\\n'.format( sp, sptag[1], raw, skim, skim/raw, cuts1, cuts1/raw)
        # CUTS 2
        if raw>0 and cuts1>0:
            output += '{0:5} & {1:12} & {2:10d} & {3:10d} & {4:10d} & {5:6.2e} & {6:6.2e} \\\\\n'.format( sp, sptag[1], raw, cuts1, cuts2,  cuts2/cuts1, cuts2/raw)

    output += '\\end{tabular}\n'
    output += '\\end{table}\n'

    print(output)
    #outMC.write(output)
#'''
################################################################################

################################################################################
#'''
for decay in decays:
    output = '\\begin{table}\n'
    output += '\\caption{Cuts flow for data for ' +decay + ' final state. Cuts are described in the text.\\label{tab:cutflow2data' +decay+ '}}\n'
    output += '\\begin{tabular}{l l r | r r | r r}\n'
    #output += '\\multicolumn{7}{c}{' + decay + '}\\\\\n'
    # CUTS 1
    #output += 'Run & & Raw events & Skim events & Skim \% & Cuts events & Cuts \% of raw \\\\\n'
    # CUTS 2
    output += 'SP & & Raw events & Previous cuts & Cuts step 2 & Cuts frac. of prev & Cuts frac. of raw \\\\\n'
    output += '\\hline\n'
    for run in runs:
        sptag = get_sptag('AllEvents'+run)
        raw = raw_event_numbers['DATA'][run]['raw']
        skim = skim_numbers['DATA'][run]['skim']
        cuts1 = cuts1_numbers['DATA'][decay][run]['cuts1']
        #cuts2 = cuts2_numbers['DATA'][decay][run]['tighterPID_childmomentum']
        cuts2 = cuts2_numbers['DATA'][decay][run]['selection_cuts']

        # CUTS 1
        #output += '{0:5} & {1:12} & {2:10d} & {3:10d} & {4:6.2e} & {5:10d} & {6:6.2e} \\\\\n'.format( run, sptag[1], raw, skim, skim/raw, cuts1, cuts1/raw)
        # CUTS 2
        if raw>0 and cuts1>0:
            output += '{0:5} & {1:12} & {2:10d} & {3:10d} & {4:10d} & {5:6.2e} & {6:6.2e} \\\\\n'.format( run, sptag[1], raw, cuts1, cuts2,  cuts2/cuts1, cuts2/raw)

    output += '\\end{tabular}\n'
    output += '\\end{table}\n'

    print(output)
    #outDATA.write(output)
#'''
################################################################################
