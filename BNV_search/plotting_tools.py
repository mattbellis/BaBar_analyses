import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns


################################################################################
def get_variable_parameters_for_plotting():
    plotvars = {}
    plotvars["nbnvbcand"] = {"values":[], "xlabel":r"# of BNV B-candidates", "ylabel":r"# E","range":(0,10)} 
    plotvars["bnvbcandmass"] = {"values":[], "xlabel":r"Mass BNV B-candidate [GeV/c$^{2}$]", "ylabel":r"# E","range":(0,9)} 
    plotvars["bnvbcandMES"] = {"values":[], "xlabel":r"BNV M$_{\rm ES}$ [GeV/c$^{2}$]", "ylabel":r"# E","range":(5.1,5.3)} 
    plotvars["bnvbcandDeltaE"] = {"values":[], "xlabel":r"BNV $\Delta E$ [GeV]", "ylabel":r"# E","range":(-5,5)} 
    plotvars["bnvprotp3"] = {"values":[], "xlabel":r"BNV proton $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,5)} 
    plotvars["bnvlepp3"] = {"values":[], "xlabel":r"BNV lepton $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,5)} 

    plotvars["p3"] = {"values":[], "xlabel":r"$|p|$ [GeV/c]", "ylabel":r"# E","range":(0,5)} 
    plotvars["cos(theta)"] = {"values":[], "xlabel":r"$\cos(\theta)$", "ylabel":r"# E","range":(-1,1)} 

    plotvars["tagbcandmass"] = {"values":[], "xlabel":r"Mass tag B-candidate [GeV/c$^{2}$]", "ylabel":r"# E","range":(0,9)} 
    plotvars["tagbcandMES"] = {"values":[], "xlabel":r"tag M$_{\rm ES}$ [GeV/c$^{2}$]", "ylabel":r"# E","range":(5.1,5.3)} 
    plotvars["tagbcandDeltaE"] = {"values":[], "xlabel":r"tag $\Delta E$ [GeV]", "ylabel":r"# E","range":(-5,5)} 
    plotvars["tagq"] = {"values":[], "xlabel":r"tag charge", "ylabel":r"# E","range":(-5,5)} 
    plotvars["missingmass"] = {"values":[], "xlabel":r"Missing mass [GeV/c$^2$]", "ylabel":r"# E","range":(-10,10)} 
    plotvars["missingmom"] = {"values":[], "xlabel":r"Missing momentum [GeV/c]", "ylabel":r"# E","range":(0,10)} 
    plotvars["missingE"] = {"values":[], "xlabel":r"Missing E [GeV]", "ylabel":r"# E","range":(-2,10)} 
    plotvars["scalarmomsum"] = {"values":[], "xlabel":r"Scalar momentum sum [GeV/c]", "ylabel":r"# E","range":(0,15)} 
    plotvars["nhighmom"] = {"values":[], "xlabel":r"# high p tracks", "ylabel":r"# E","range":(0,5)} 
    plotvars["np"] = {"values":[], "xlabel":r"# proton", "ylabel":r"# E","range":(0,5)} 
    plotvars["nmu"] = {"values":[], "xlabel":r"# muon", "ylabel":r"# E","range":(0,5)} 
    plotvars["ne"] = {"values":[], "xlabel":r"# electron", "ylabel":r"# E","range":(0,5)} 
    plotvars["pp"] = {"values":[], "xlabel":r"proton $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4)} 
    plotvars["mup"] = {"values":[], "xlabel":r"muon $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4)} 
    plotvars["ep"] = {"values":[], "xlabel":r"electron $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4)} 
    plotvars["r2"] = {"values":[], "xlabel":r"R2", "ylabel":r"# E","range":(0,1)} 
    plotvars["r2all"] = {"values":[], "xlabel":r"R2 all", "ylabel":r"# E","range":(0,1)} 
    plotvars["thrustmag"] = {"values":[], "xlabel":r"Thrust mag", "ylabel":r"# E","range":(0,1)} 
    plotvars["thrustmagall"] = {"values":[], "xlabel":r"Thrust mag all", "ylabel":r"# E","range":(0,1)} 
    plotvars["thrustcosth"] = {"values":[], "xlabel":r"Thrust $\cos(\theta)$", "ylabel":r"# E","range":(-1,1)} 
    plotvars["thrustcosthall"] = {"values":[], "xlabel":r"Thrust $\cos(\theta)$ all", "ylabel":r"# E","range":(-1,1)} 
    plotvars["sphericityall"] = {"values":[], "xlabel":r"Sphericity all", "ylabel":r"# E","range":(0,1)} 
    plotvars["ncharged"] = {"values":[], "xlabel":r"# charged particles", "ylabel":r"# E","range":(0,20)} 
    plotvars["nphot"] = {"values":[], "xlabel":r"# photons","ylabel":r"# E","range":(0,20)} 

    # Make the plotvars for the PID flags
    particles = ['proton','e','mu']
    flags = ['IsTightKMProton',
             'IsVeryTightKMProton',
             'IsSuperTightKMProton',
             'IsTightBDTKaon',
             'IsVeryTightBDTKaon',
             'IsTightKMKaon',
             'IsVeryTightKMKaon',
             'IsSuperTightKMKaon',
             'IsTightKMPion',
             'IsVeryTightKMPion',
             'IsSuperTightKMPion',
             'IsTightKMElectron',
             'IsVeryTightKMElectron',
             'IsSuperTightKMElectron',
             'IsBDTTightMuon',
             'IsBDTVeryTightMuon',
             'IsBDTTightMuonFakeRate',
             'IsBDTVeryTightMuonFakeRate']

    for particle in particles:
        for flag in flags:
            name = '{0}{1}'.format(particle,flag)
            plotvars[name] = {"values":[], "xlabel":name,"ylabel":r"#","range":(-2,2)} 

    return plotvars


################################################################################
def make_all_plots(dfs,specific_plots=[],backend='seaborn',grid_of_plots=(2,2),kde=False,plot_params=None,figsize=(9,7),norm_hist=False,infilenames=None,xlabelfontsize=12,ignorePID=False):

    if type(dfs) != list:
        dfs = [dfs]

    if plot_params is None:
        plot_params = get_variable_parameters_for_plotting()

    tempnames = dfs[0].columns.values
    names = []
    if ignorePID:
        for name in tempnames:
            if name.find('Is')>=0 or name.find('BDT')>=0 or name.find('KM')>=0:
                1
            else:
                names.append(name)

    nplots = len(names)

    nplots_per_figure = grid_of_plots[0]*grid_of_plots[1]

    grid_count = 0
    for i,name in enumerate(names):

        if len(specific_plots)>0 and name not in specific_plots:
            continue

        if i%nplots_per_figure==0:
            plt.figure(figsize=figsize)
            grid_count = 0

        plt.subplot(grid_of_plots[0],grid_of_plots[1],grid_count+1)

        plotrange=None
        xlabel=None
        bins=100
        if name in plot_params.keys():
            xlabel = plot_params[name]['xlabel']
            plotrange = plot_params[name]['range']

        if name.find('Is')>=0 or name.find('BDT')>=0 or name.find('KM')>=0:
            plotrange=(0,1)
            bins=2
        
        if backend=='seaborn':
            if plotrange is not None:
                for j,df in enumerate(dfs):
                    label = None
                    if infilenames is not None:
                        label = infilenames[j]
                    sns.distplot(df[name],bins=bins,hist_kws={"range": plotrange},kde=kde,norm_hist=norm_hist,label=label)
                    plt.xlim(plotrange[0],plotrange[1])
            else:
                for j,df in enumerate(dfs):
                    label = None
                    if infilenames is not None:
                        label = infilenames[j]
                    sns.distplot(df[name],bins=bins,kde=kde,norm_hist=norm_hist,label=label)

            if xlabel is not None:
                plt.xlabel(xlabel,fontsize=xlabelfontsize)
            else:
                plt.xlabel(name,fontsize=xlabelfontsize)

            if infilenames is not None:
                plt.legend(fontsize=8)


        if i%nplots_per_figure==nplots_per_figure-1 or i==nplots-1:
            print("Here!")
            plt.tight_layout()

        grid_count += 1




