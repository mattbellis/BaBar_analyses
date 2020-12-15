import matplotlib.pylab as plt
import numpy as np
import sys
import pandas as pd
import seaborn as sns

import plotting_tools as pt
import babar_dataframe_tools as bd
#import babar_tools as bt


#raw = pt.return_dataset_information(verbose=True)


#########################
from raw_event_numbers_and_cross_section import *# raw_event_numbers as raw
#raw = raw_event_numbers

tot = 0
for key in raw_event_numbers["DATA"].keys():
	tot += raw_event_numbers["DATA"][key]["raw"]

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

	print("{0:4s} {1:6.2f} {2:9.2f} {3:9.2f} {4:9.2f} {5:9.2f} {6:9.2f}".format(key, xsec, xsec*intlumi, raw/1e6, (raw/1e6)/(xsec*intlumi), weight, 1/weight))
	tot += xsec

print(tot)

raw = raw_event_numbers
####################

infilenames = sys.argv[1:]

#raw["MC"]["9456"]["weight"] = 0.001

decay = None
decays = ['pmu', 'pe', 'pnu', 'nmu', 'ne']
for d in decays:
    if infilenames[0].find(d)>=0:
        decay = d
        break

PID_mask_FLAGS = []
if decay=='pmu' or decay=='pe' or decay=='pnu':
    PID_mask_FLAGS.append('proton')
if decay=='pmu' or decay=='nmu':
    PID_mask_FLAGS.append('muon')
if decay=='pe' or decay=='ne':
    PID_mask_FLAGS.append('electron')

dfs = []
sps = []
labels = []
weights = []
colors = []
for icount,infilename in enumerate(infilenames):

    if infilename.find('.csv')>=0:
        df = pd.read_csv(infilename)
    elif infilename.find('.h5')>=0:
        df = pd.read_hdf(infilename)


    if icount==0:
        print(df.columns)
    #lepton_mask = bd.pid_mask(df,particle='muon')
    #lepton_mask = bd.pid_mask(df,particle='electron')
    #lepton_mask = bd.pid_mask(df,particle='proton')
    #proton_mask = bd.pid_mask(df,particle='proton')
    #proton_mask = bd.pid_mask(df,particle='proton')
    #proton_mask = bd.pid_mask(df,particle='muon')
    #proton_mask = bd.pid_mask(df,particle='electron')

	
    if decay=='pmu':
        pid_mask = bd.pid_mask(df,particle='proton') & bd.pid_mask(df,particle='muon')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='muon')
    elif decay=='pe':
        pid_mask = bd.pid_mask(df,particle='proton') & bd.pid_mask(df,particle='electron')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='electron')
    elif decay=='pnu':
        pid_mask = bd.pid_mask(df,particle='proton')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='nu')
    elif decay=='nmu':
        pid_mask = bd.pid_mask(df,particle='muon')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='muon')
    elif decay=='ne':
        pid_mask = bd.pid_mask(df,particle='electron')
        bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='electron')

    shape_mask = bd.shape_mask(df)
    #print(df.columns)

    blinding_mask = bd.blinding_mask(df)

    #side_bands_mask = bd.side_bands_mask(df,region='DeltaEmES')
    #side_bands_mask = bd.side_bands_mask(df,region='protonp3')

    #bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton')
    #bnv_children_momentum_mask = bd.bnv_children_momentum_mask(df,child='proton') & bd.bnv_children_momentum_mask(df,child='electron')

    #dfs.append(df)
    #print("------------")
    #print("Total:    ", len(df))
    #print("Lepton:   ", len(df[lepton_mask]))
    #print("Lepton:   ", len(df[lepton_mask])/len(df))
    #print("Proton:   ", len(df[proton_mask]))
    #print("Proton:   ", len(df[proton_mask])/len(df))
    #print("Lep&Prot: ", len(df[lepton_mask & proton_mask]))
    #print("Lep&Prot: ", len(df[lepton_mask & proton_mask])/len(df))
    ##print("Sideband: ", len(df[side_bands_mask]))
    ##print("Sideband: ", len(df[side_bands_mask])/len(df))
    ##print(len(df[shape_mask & lepton_mask & proton_mask])/len(df))
    #print("------------")

    #df_mu = df[lepton_mask]
    #dfs.append(df_mu)
    #df_proton = df[proton_mask]
    #dfs.append(df_proton)
    #df_both = df[lepton_mask & proton_mask]
    #dfs.append(df_both)

    #dftmp = df[shape_mask & proton_mask & lepton_mask]
    #dftmp = df[proton_mask & lepton_mask]
    #dfs.append(dftmp)

    # No cuts
    #dfs.append(df)

    #dftmp = df[proton_mask & lepton_mask & ~blinding_mask]
    #dftmp = df[proton_mask & lepton_mask & side_bands_mask]
    #dftmp = df[proton_mask & lepton_mask & bnv_children_momentum_mask]
    #dftmp = df[pid_mask & bnv_children_momentum_mask]
    #dftmp = df[pid_mask & bnv_children_momentum_mask & (df['ncharged']>5) & (df['ne']==1) & (df['sphericityall']>0.02) & (df['thrustmagall']<0.92) & (df['thrustmagall']<0.92) ]
    #dftmp = df[pid_mask & bnv_children_momentum_mask & (df['sphericityall']>0.02)  ]
    #dftmp = df[bnv_children_momentum_mask & (df['sphericityall']>0.02) & (df['ne']==1)   & (df['ncharged']>5) & shape_mask   ]
    dftmp = None
    if infilenames[0].find('AllEvents')>=0:
        dftmp = df[pid_mask & bnv_children_momentum_mask & ~blinding_mask ]
    else:
        dftmp = df[pid_mask & bnv_children_momentum_mask ]
    dfs.append(dftmp)

    print(infilename)
    sp,label = pt.get_sptag(infilename)
    print(sp,label)
    sps.append(sp)
    labels.append(label)

    wt = 1.0
    print(sp)
    if sp.find('Run')<0 and sp.find('runs')<0:
        if 'weight' in list(raw['MC'][sp].keys()):
            wt = raw['MC'][sp]['weight']
    print(wt)
    weights.append(wt)
    #weights.append(wt)
    colors.append(pt.get_color_scheme(sp))
    #colors.append('r')

# Use this for testing cuts
#labels = ['PID cuts','shape cuts']
#weights = [1.0, 1.0]
#colors = ['k','g']

print("Making the plots.......")
plot_params = pt.get_variable_parameters_for_plotting()
# pe and pmu
#plot_params['bnvbcandDeltaE']['range'] = (-1.0,1.0)
#plot_params['bnvbcandDeltaE']['range'] = (-3.0,-2.0)
#plot_params['bnvbcandDeltaE']['range'] = (-4.0,-2.0)
plot_params['bnvbcandMES']['range'] = (5.2,5.3)
#pt.make_all_plots(dfs,grid_of_plots=(4,4),xlabelfontsize=10,ignorePID=True,norm_hist=True,labels=labels,plot_params=plot_params)
#pt.make_all_plots(dfs,grid_of_plots=(4,4),xlabelfontsize=10,ignorePID=True,plot_params=plot_params,labels=labels,stacked=False,weights=weights)

# For overlaying the data - STILL IN TESTING STATE
#pt.make_all_plots(dfs,backend='matplotlib',grid_of_plots=(4,4),xlabelfontsize=10,ignorePID=True,plot_params=plot_params,labels=labels,stacked=True,weights=weights,color=colors,overlay_data=True)

############### USE THIS FOR MC STACKING ##############
# For stacked histograms
#pt.make_all_plots(dfs,backend='matplotlib',grid_of_plots=(3,3),xlabelfontsize=10,ignorePID=True,plot_params=plot_params,labels=labels,stacked=True,weights=weights,color=colors,figsize=(12,7))
#specific_plots = ['bnvbcandDeltaE','bnvbcandMES','tagbcandDeltaE','tagbcandMES']
# Shape
specific_plots = ['thrustmag','thrustcosth','thrustmagall','thrustcosthall', 'sphericityall','r2','r2all','nphot','ncharged','missingE','missingmom','missingmass','scalarmomsum','bnvprotp3','bnvlepp3', 'ne','nmu','np','nbnvbcand']
specific_plots += ['bnvbcandDeltaE','bnvbcandMES','tagbcandDeltaE','tagbcandMES']
# For documentation
specific_plots = ['thrustmag','thrustcosth','thrustmagall','thrustcosthall', \
                  'sphericityall','r2','r2all','scalarmomsum', \
                   'bnvbcandDeltaE','bnvbcandMES','tagbcandDeltaE','tagbcandMES', \
                  'missingE','missingmom','missingmass']

#pt.make_all_plots(dfs,specific_plots=specific_plots,backend='matplotlib',grid_of_plots=(1,4),xlabelfontsize=10,ignorePID=True,plot_params=plot_params,labels=labels,sps=sps,stacked=True,weights=weights,color=colors,figsize=(15,3), overlay_data=True, decay=decay)
#plt.savefig('plots/summary_plots_bkg_pmu.png')
#plt.savefig('plots/summary_plots_sig_pmu.png')
#plt.savefig('plots/summary_plots_bkg_pnu.png')
#plt.savefig('plots/summary_plots_sig_pnu.png')
#plt.savefig('plots/summary_plots_sig_nmu.png')
#plt.savefig('plots/summary_plots_bkg_nmu.png')

# MES vs DeltaE
pt.plot_mes_vs_de(dfs,bins=100,ranges=((5.2,5.3),(-0.5,0.5)),decay=decay,labels=labels,sps=sps)#,xlabelfontsize=12,alpha=0.5,color='k', markersize=1, decay=None, tag='default'):

# For comparing cuts
#pt.make_all_plots(dfs,backend='matplotlib',grid_of_plots=(3,3),xlabelfontsize=10,ignorePID=True,plot_params=plot_params,labels=labels,stacked=False,weights=weights,color=colors,figsize=(12,7),norm_hist=True)
#pt.make_all_plots(dfs,backend='matplotlib',grid_of_plots=(3,3),xlabelfontsize=10,ignorePID=True,plot_params=plot_params,labels=labels,stacked=False,weights=weights,color=colors,figsize=(12,7),norm_hist=False)

#plot_params = pt.get_variable_parameters_for_plotting()
#plot_params['p3']['range'] = (2.0,3.0)
#pt.make_all_plots(dfs,specific_plots=['p3','cos(theta)'],grid_of_plots=(1,1),plot_params=plot_params,figsize=(4,3),norm_hist=True,labels=labels)

#plt.show()
