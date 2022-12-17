import matplotlib.pylab as plt
import numpy as np
import sys
import pandas as pd
import seaborn as sns

import plotting_tools as pt
import babar_dataframe_tools as bd
#import babar_tools as bt

raw = pt.return_dataset_information(verbose=True)

color_scheme = {'1235':'b', 
                '1237':'c', 
                '998':'g', 
                '1005':'r', 
                '3429':'m', 
                '9456':'k', 
                'All runs':'k', 
                }

infilenames = sys.argv[1:]

dfs = []
sps = []
labels = []
weights = []
colors = []

for infilename in infilenames:

    if infilename.find('.csv')>=0:
        df = pd.read_csv(infilename)
    elif infilename.find('.h5')>=0:
        df = pd.read_hdf(infilename)

    sp,label,decay = pt.get_sptag(infilename)
    print(sp,label,decay)
    sps.append(label)
    labels.append(label)

    #muon_mask = bd.pid_mask(df,particle='muon')
    #proton_mask = bd.pid_mask(df,particle='proton')
    #shape_mask = bd.shape_mask(df)

    #dsc_mask = bd.decay_specific_cuts(df,decay='pmu')
    dsc_mask = bd.decay_specific_cuts(df,decay='pe')
    blinding_mask = bd.blinding_mask(df)
    dftmp = df[dsc_mask]# & ~blinding_mask ]

    dfs.append(dftmp)

    #df_mu = df[muon_mask]
    #dfs.append(df_mu)
    #df_proton = df[proton_mask]
    #dfs.append(df_proton)
    #df_both = df[muon_mask & proton_mask & shape_mask]
    #dfs.append(df_both)

    wt = 1.0
    '''
    #print(sp)
    #print(list(raw['MC'].keys()))
    if 'weight' in list(raw['MC'][sp].keys()):
        wt = raw['MC'][sp]['weight']
    #print(wt)
    '''
    weights.append(wt)
    colors.append(color_scheme[sp])


plot_params = pt.get_variable_parameters_for_plotting()
plot_params['bnvbcandDeltaE']['range'] = (-1.0,1.0)
plot_params['bnvbcandMES']['range'] = (5.2,5.3)
for label,df in zip(labels,dfs):
    x = df['bnvbcandMES']
    y = df['bnvbcandDeltaE']

    alpha = 0.2
    mask = (x>5.265) & (y>-0.12) & (y<0.12)

    a = len(x)
    b = len(x[mask])
    print(a,b,b/a)

    for i in [1,2]:
        plt.figure()
        if i==1:
            #plt.plot(x,y,'.',markersize=1,label=label,alpha=alpha)
            pt.hist2d(x,y,xbins=100,ybins=100,xrange=(5.2,5.3),yrange=(-0.5,0.5))
        else:
            #plt.plot(x[~mask],y[~mask],'.',markersize=1,label=label,alpha=alpha)
            pt.hist2d(x[~mask],y[~mask],xbins=100,ybins=100,xrange=(5.2,5.3),yrange=(-0.5,0.5))
        plt.xlim(5.2,5.3)
        plt.ylim(-0.5,0.5)
        plt.title(label)
        plt.legend()


    # Try to figure out what's in the region
    maskA = (x>5.265) & (y>0.12) & (y<0.2)
    maskB = (x>5.265) & (y<-0.12) & (y>-0.2)

    bkgA = len(x[maskA])
    bkgB = len(x[maskB])
    avg = np.mean([bkgA,bkgB])
    print(f'bkgA: {bkgA} bkgB: {bkgB}  avg: {avg}  nentries: {b}  nentries/avg: {b/avg}')

plt.show()
