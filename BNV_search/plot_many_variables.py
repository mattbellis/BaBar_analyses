import matplotlib.pylab as plt
import numpy as np
import sys
import pandas as pd
import seaborn as sns

import plotting_tools as pt
import babar_dataframe_tools as bd
import babar_tools as bt

raw = bt.return_dataset_information(verbose=True)

infilenames = sys.argv[1:]

dfs = []
sps = []
labels = []
weights = []
for infilename in infilenames:

    if infilename.find('.csv')>=0:
        df = pd.read_csv(infilename)
    elif infilename.find('.h5')>=0:
        df = pd.read_hdf(infilename)

    muon_mask = bd.pid_mask(df,particle='muon')
    proton_mask = bd.pid_mask(df,particle='proton')

    #dfs.append(df)

    #df_mu = df[muon_mask]
    #dfs.append(df_mu)
    #df_proton = df[proton_mask]
    #dfs.append(df_proton)
    df_both = df[muon_mask & proton_mask]
    dfs.append(df_both)

    sp,label = bt.get_sptag(infilename)
    print(sp,label)
    sps.append(label)
    labels.append(label)

    wt = raw['MC'][sp]['weight']
    print(wt)
    weights.append(wt)


plot_params = pt.get_variable_parameters_for_plotting()
plot_params['bnvbcandDeltaE']['range'] = (-1.0,1.0)
plot_params['bnvbcandMES']['range'] = (5.2,5.3)
#pt.make_all_plots(dfs,grid_of_plots=(4,4),xlabelfontsize=10,ignorePID=True,norm_hist=True,labels=labels,plot_params=plot_params)
pt.make_all_plots(dfs,grid_of_plots=(4,4),xlabelfontsize=10,ignorePID=True,plot_params=plot_params,labels=labels)

#plot_params = pt.get_variable_parameters_for_plotting()
#plot_params['p3']['range'] = (2.0,3.0)
#pt.make_all_plots(dfs,specific_plots=['p3','cos(theta)'],grid_of_plots=(1,1),plot_params=plot_params,figsize=(4,3),norm_hist=True,labels=labels)

plt.show()
