import numpy as np
import matplotlib.pylab as plt

import sys

#import pickle
import uproot

import plotting_tools as pt

################################################################################

# RUN OVER FILES IN THE PID_assignment subdirectory

# Variables of interest
pars = pt.get_variable_parameters_for_plotting()

voi = ['ncharged','pp','ep','mup']


values = {}
for v in voi:
    values[v] = []

infilenames = sys.argv[1:]

sptag = pt.get_sptag(infilenames[0])


print(sptag)

for infile in infilenames:
    file = uproot.open(infile)
    print("Loading " + infile)
    tree = file['Tskim']
    #print(tree.keys())
    for v in voi:
        if v == 'pp':
            px = tree['protonpx'].array()
            py = tree['protonpy'].array()
            pz = tree['protonpz'].array()
            p = np.sqrt(px*px + py*py + pz*pz)
            values[v] += p.flatten().tolist()
        elif v == 'ep':
            px = tree['epx'].array()
            py = tree['epy'].array()
            pz = tree['epz'].array()
            p = np.sqrt(px*px + py*py + pz*pz)
            values[v] += p.flatten().tolist()
        elif v == 'mup':
            px = tree['mupx'].array()
            py = tree['mupy'].array()
            pz = tree['mupz'].array()
            p = np.sqrt(px*px + py*py + pz*pz)
            values[v] += p.flatten().tolist()
        elif v == 'ncharged':
            npi = tree['npi'].array()
            nk = tree['nk'].array()
            nproton = tree['nproton'].array()
            ne = tree['ne'].array()
            nmu = tree['nmu'].array()

            nc = npi + nk + nproton + ne + nmu

            values['ncharged'] += nc.tolist()





    #sptag = infile.split('OUTPUT_')[1].split('.pkl')[0]
    #sptag = infile.split('_')[2].split('.pkl')[0]
    #allplotvars[sptag] = x


plt.figure(figsize=(16,3))
for i,v in enumerate(voi):
    plt.subplot(1,4,i+1)
    #print(v,pars[v])
    xlabel = pars[v]['xlabel']
    ylabel = '# of events' #pars[v]['ylabel']
    r = pars[v]['range']
    bins = pars[v]['bins']
    x = values[v]
    color = pt.get_color_scheme(sptag[0])
    #print(color)
    #print(x)
    plt.hist(x,range=r,bins=bins,color=color,label=sptag[1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if v=='ncharged':
        y = np.array(x)
        tot = len(y)
        print(tot, len(y[y>=3])/tot, len(y[y>=5])/tot)

plt.legend(fontsize=12)
plt.tight_layout()

filename = 'plots/before_any_cuts_ncharged_momentum_{0}.png'.format(sptag[0])
plt.savefig(filename)
plt.show()

