import numpy as np
import matplotlib.pylab as plt

import sys

import pickle

import plotting_tools as pt

################################################################################

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
    print("Loading " + infile)
    data = pickle.load(open(infile,'rb'))
    print(data.keys())
    for v in voi:
        values[v] += data[v]['values'][0]
        #values = data[v][0]
        #print(values)



    #sptag = infile.split('OUTPUT_')[1].split('.pkl')[0]
    #sptag = infile.split('_')[2].split('.pkl')[0]
    #allplotvars[sptag] = x


plt.figure(figsize=(16,3))
for i,v in enumerate(voi):
    plt.subplot(1,4,i+1)
    print(v,pars[v])
    xlabel = pars[v]['xlabel']
    ylabel = '# of events' #pars[v]['ylabel']
    r = pars[v]['range']
    bins = pars[v]['bins']
    x = values[v]
    color = pt.get_color_scheme(sptag[0])
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

