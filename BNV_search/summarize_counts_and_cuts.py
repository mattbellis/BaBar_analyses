import numpy as np
import matplotlib.pylab as plt

import sys

from raw_event_numbers_and_cross_section import raw_event_numbers
from selection_numbers import event_numbers as skim_numbers
from selection_numbers_after_cuts1 import event_numbers as cuts1_numbers
from plotting_tools import get_sptag

datatypes = ['DATA','MC']
decays = ['pmu', 'pe', 'pnu', 'nmu', 'ne']
sps = ['9456', '9457', '11975', '11976', '11977' ,'1235', '1237', '1005', '998', '3429']
runs = ['Run1', 'Run2', 'Run3', 'Run4', 'Run5', 'Run6']

output = '\\begin{table}\n'
output += '\\begin{tabular}{l l r r r}\n'
for decay in decays:
    output += '\\multicolumn{5}{c}{' + decay + '}\\\\\n'
    for sp in sps:
        sptag = get_sptag('SP'+sp)
        raw = raw_event_numbers['MC'][sp]['raw']
        skim = skim_numbers['MC'][sp]['skim']
        cuts1 = cuts1_numbers['MC'][decay][sp]['cuts1']

        #print('{0:3} {1:5} {2:10d} {3:8.3e} {4:8.3e}'.format( decay, sp, raw, skim/raw, cuts1/raw))
        output += '{0:5} & {1:12} & {2:10d} & {3:10d} & {4:10d} \\\\\n'.format( sp, sptag[1], raw, skim, cuts1)

output += '\\end{tabular}\n'
output += '\\end{table}\n'

print(output)
