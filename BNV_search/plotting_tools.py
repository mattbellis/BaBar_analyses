import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns


################################################################################
def get_variable_parameters_for_plotting():
    plotvars = {}
    plotvars["nbnvbcand"] = {"values":[], "xlabel":r"# of BNV B-candidates", "ylabel":r"# E","range":(0,10)} 
    plotvars["bnvbcandmass"] = {"values":[], "xlabel":r"Mass BNV B-candidate [GeV/c$^{2}$]", "ylabel":r"# E","range":(0,9)} 
    plotvars["bnvbcandp3"] = {"values":[], "xlabel":r"|p| BNV B-candidate [GeV/c]", "ylabel":r"# E","range":(0,6)} 
    plotvars["bnvbcandMES"] = {"values":[], "xlabel":r"BNV M$_{\rm ES}$ [GeV/c$^{2}$]", "ylabel":r"# E","range":(5.1,5.3)} 
    plotvars["bnvbcandDeltaE"] = {"values":[], "xlabel":r"BNV $\Delta E$ [GeV]", "ylabel":r"# E","range":(-5,5)} 
    plotvars["bnvprotp3"] = {"values":[], "xlabel":r"BNV baryon $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,5)} 
    plotvars["bnvlepp3"] = {"values":[], "xlabel":r"BNV lepton $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,5)} 
    plotvars["bnvprotcosth"] = {"values":[], "xlabel":r"BNV baryon $\cos(\theta)$ ", "ylabel":r"# E","range":(-1.1,1.1)} 
    plotvars["bnvlepcosth"] = {"values":[], "xlabel":r"BNV lepton $\cos(\theta)$ ", "ylabel":r"# E","range":(-1.1,1.1)} 

    plotvars["p3"] = {"values":[], "xlabel":r"$|p|$ [GeV/c]", "ylabel":r"# E","range":(0,5)} 
    plotvars["cos(theta)"] = {"values":[], "xlabel":r"$\cos(\theta)$", "ylabel":r"# E","range":(-1,1)} 

    plotvars["tagbcandmass"] = {"values":[], "xlabel":r"Mass tag B-candidate [GeV/c$^{2}$]", "ylabel":r"# E","range":(0,9)} 
    plotvars["tagbcandMES"] = {"values":[], "xlabel":r"tag M$_{\rm ES}$ [GeV/c$^{2}$]", "ylabel":r"# E","range":(5.1,5.3)} 
    plotvars["tagbcandDeltaE"] = {"values":[], "xlabel":r"tag $\Delta E$ [GeV]", "ylabel":r"# E","range":(-5,5)} 
    plotvars["tagbcandp3"] = {"values":[], "xlabel":r"|p| tag B-candidate [GeV/c]", "ylabel":r"# E","range":(0,6)} 
    plotvars["tagq"] = {"values":[], "xlabel":r"tag charge", "ylabel":r"# E","range":(-5,5)} 
    plotvars["missingmassES"] = {"values":[], "xlabel":r"Missing mass ES$^2$ [GeV$^2$/c$^4$]", "ylabel":r"# E","range":(-10,10)} 
    plotvars["missingmass2"] = {"values":[], "xlabel":r"Missing mass$^2$ [GeV$^2$/c$^4$]", "ylabel":r"# E","range":(-5,5)} 
    plotvars["missingmass2_byhand"] = {"values":[], "xlabel":r"Missing mass$^2$ (by hand) [GeV$^2$/c$^4$]", "ylabel":r"# E","range":(-5,5)} 
    plotvars["missingmass_byhand"] = {"values":[], "xlabel":r"Missing mass (by hand) [GeV/c$^2$]", "ylabel":r"# E","range":(-5,5)} 
    plotvars["missingmom"] = {"values":[], "xlabel":r"Missing momentum [GeV/c]", "ylabel":r"# E","range":(0,10)} 
    plotvars["missingE"] = {"values":[], "xlabel":r"Missing E [GeV]", "ylabel":r"# E","range":(-2,10)} 
    plotvars["scalarmomsum"] = {"values":[], "xlabel":r"Scalar momentum sum [GeV/c]", "ylabel":r"# E","range":(0,15)} 
    plotvars["nhighmom"] = {"values":[], "xlabel":r"# high p tracks", "ylabel":r"# E","range":(0,5),"bins":5} 
    plotvars["np"] = {"values":[], "xlabel":r"# proton", "ylabel":r"# E","range":(0,5),"bins":5} 
    plotvars["nmu"] = {"values":[], "xlabel":r"# muon", "ylabel":r"# E","range":(0,5),"bins":5} 
    plotvars["ne"] = {"values":[], "xlabel":r"# electron", "ylabel":r"# E","range":(0,5),"bins":5} 
    plotvars["pp"] = {"values":[], "xlabel":r"proton $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4),"bins":100} 
    plotvars["mup"] = {"values":[], "xlabel":r"muon $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4),"bins":100} 
    plotvars["ep"] = {"values":[], "xlabel":r"electron $|p|$ [GeV/c]", "ylabel":r"# E","range":(0,4),"bins":100}
    plotvars["r2"] = {"values":[], "xlabel":r"R2", "ylabel":r"# E","range":(0,1.2)} 
    plotvars["r2all"] = {"values":[], "xlabel":r"R2 all", "ylabel":r"# E","range":(0,1.2)} 
    plotvars["thrustmag"] = {"values":[], "xlabel":r"Thrust mag", "ylabel":r"# E","range":(0,1.2)} 
    plotvars["thrustmagall"] = {"values":[], "xlabel":r"Thrust mag all", "ylabel":r"# E","range":(0,1.2)} 
    plotvars["thrustcosth"] = {"values":[], "xlabel":r"Thrust $\cos(\theta)$", "ylabel":r"# E","range":(-0.2,1.2)} 
    plotvars["thrustcosthall"] = {"values":[], "xlabel":r"Thrust $\cos(\theta)$ all", "ylabel":r"# E","range":(-0.2,1.2)} 
    plotvars["sphericityall"] = {"values":[], "xlabel":r"Sphericity all", "ylabel":r"# E","range":(0,1.2)} 
    plotvars["ncharged"] = {"values":[], "xlabel":r"# charged particles", "ylabel":r"# E","range":(0,20),"bins":20} 
    plotvars["nphot"] = {"values":[], "xlabel":r"# photons","ylabel":r"# E","range":(0,20),"bins":20} 

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
def get_color_scheme(sp=None):

    color_scheme = {'1235':'b', 
                    '1237':'c', 
                    '980':'darkcyan', 
                    '998':'g', 
                    '1005':'r', 
                    '3429':'m', 
                    '3981':'sandybrown', 
                    '2400':'lawngreen', 
                    '9456':'k', 
                    '9457':'k', 
                    '11975':'k', 
                    '11976':'k', 
                    '11977':'k', 
                    'Run1':'k', 
                    'Run2':'k', 
                    'Run3':'k', 
                    'Run4':'k', 
                    'Run5':'k', 
                    'Run6':'k', 
                    'All runs':'k', 
                    }

    if sp==None:
        return color_scheme
    else:
        return color_scheme[sp]

################################################################################
def plot_mes_vs_de(dfs,specific_plots=['bnvbcandMES','bnvbcandDeltaE'],plot_params=None,figsize=(5,3.5),ranges=None,bins=None,labels=None,sps=None,xlabelfontsize=12,alpha=0.5,color='k', markersize=1, decay=None, tag='default'):

    plotvars = get_variable_parameters_for_plotting()

    axeslabels = []
    axeslabels.append(plotvars[specific_plots[0]]['xlabel'])
    axeslabels.append(plotvars[specific_plots[1]]['xlabel'])

    if ranges is None:
        ranges = []
        ranges.append(plotvars[specific_plots[0]]['range'])
        ranges.append(plotvars[specific_plots[1]]['range'])

    #plt.figure(figsize=figsize)
    #plt.subplot(1,1,1)

    for df in dfs:
        # Need this as per
        # https://stackoverflow.com/questions/51953869/convenient-way-to-deal-with-valueerror-cannot-reindex-from-a-duplicate-axis
        df = df.reset_index()

        x = df[specific_plots[0]]
        y = df[specific_plots[1]]

        print(df.columns)

        #plt.plot(x,y,'.',markersize=markersize)
        #'''
        print("LABELS: ",labels)
        print(df[specific_plots[0]].values)
        print(df[specific_plots[1]].values)
        print(len(df[specific_plots[0]].values))
        print(len(df[specific_plots[1]].values))
        print(ranges[0], ranges[1])
        print(bins)
        #sns.histplot(df,x=specific_plots[0],y=specific_plots[1],binrange=(ranges[0],ranges[1]),bins=bins,cbar=True)#,ax=plt.gca())
        #sns.jointplot(data=df,x=specific_plots[0],y=specific_plots[1],kind="hist",marginal_kws={"bins":25})#,ax=plt.gca())
        #sns.jointplot(data=df,x=specific_plots[0],y=specific_plots[1],marginal_kws={"bins":25})#,ax=plt.gca())
        #sns.jointplot(data=df,x=specific_plots[0],y=specific_plots[1],kind="hist",joint_kws={"bins":100},marginal_kws={"bins":25})#,ax=plt.gca())
        sns.jointplot(data=df,x=specific_plots[0],y=specific_plots[1],joint_kws={"alpha":0.05})#, "size":1},marginal_kws={"bins":25})#,ax=plt.gca())
        plt.xlabel(axeslabels[0],fontsize=xlabelfontsize)
        plt.ylabel(axeslabels[1],fontsize=xlabelfontsize)
        plt.title(label=labels[0])
        #'''

    print("HER---------------------------------")
    plt.tight_layout()

    # MC
    filename = 'plots/de_vs_mes_cut_summary_files_SP-{0}_{1}_{2}.png'.format(sps[0],decay,tag)
    # Data
    if sps[0].find('runs')>=0:
        filename = 'plots/de_vs_mes_cut_summary_files_{0}_{1}_{2}.png'.format(labels[0],decay,tag)
    print(filename)
    plt.savefig(filename)

################################################################################
def make_all_plots(df_plotting_container,specific_plots=[],backend='matplotlib',grid_of_plots=(2,2),kde=False,plot_params=None,figsize=(9,7),norm_hist=False,xlabelfontsize=12,ignorePID=False,stacked=False,alpha=0.5,decay=None, tag='default'):

    if plot_params is None:
        plot_params = get_variable_parameters_for_plotting()

    sps_in_container = list(df_plotting_container.keys())
    print(sps_in_container)
    tempdf = df_plotting_container[sps_in_container[0]]['df']
    tempnames = None
    if type(tempdf) is list:
        tempnames = tempdf[0].columns
    else:
        tempnames = tempdf.columns
    #tempnames = df_plotting_container[sps_in_container[0]]['dfs'][0].columns

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
    i = 0
    if len(specific_plots) == 0:
        specific_plots = list(names)

    figcount = 0

    sps_for_labels = []

    #for icount,name in enumerate(names):
    for icount,name in enumerate(specific_plots):

        #if len(specific_plots)>0 and name not in specific_plots:
        if name not in names:
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
            if 'bins' in list(plot_params[name].keys()):
                bins = plot_params[name]['bins']

        if name.find('Is')>=0 or name.find('BDT')>=0 or name.find('KM')>=0:
            plotrange=(0,1)
            bins=2
        
        ########################################################################
        '''
        if backend=='seaborn':
            if plotrange is not None:
                for j,df in enumerate(dfs):
                    label = None
                    if labels is not None:
                        label = labels[j]
                    weight=np.ones(len(df[name]))
                    if type(weights) == list:
                        weight *= weights[j]

                    sns.distplot(df[name],bins=bins,hist_kws={"range": plotrange, "weights":weight, "stacked":stacked,'alpha':alpha},kde=kde,norm_hist=norm_hist,label=label)
                    plt.xlim(plotrange[0],plotrange[1])
            else:
                for j,df in enumerate(dfs):
                    label = None
                    if labels is not None:
                        label = labels[j]
                    weight=np.ones(len(df[name]))
                    if type(weights) == list:
                        weight *= weights[j]

                    sns.distplot(df[name],bins=bins,kde=kde,norm_hist=norm_hist,label=label,hist_kws={"weights":weight, "stacked":stacked})

            if xlabel is not None:
                plt.xlabel(xlabel,fontsize=xlabelfontsize)
            else:
                plt.xlabel(name,fontsize=xlabelfontsize)

            if labels is not None:
                plt.legend(fontsize=8)

        '''
        ########################################################################
        if backend=='matplotlib':
            #if plotrange is not None:
            allvals = []
            allweights=[]
            #last_df = len(dfs)

            backgroundMC = {'values': [], 'weights': [], 'colors': [], 'labels': []}
            signalMC = {'values': [], 'weights': [], 'colors': [], 'labels': []}
            data = {'values': [], 'weights': [], 'colors': [], 'labels': []}

            totweights = 0
            for sp in sps_in_container:
                c = df_plotting_container[sp]
                if c['isSignalMC'] is True:
                    signalMC['values'] = c['df'][name]
                    signalMC['colors'] = c['color']
                    signalMC['weights'] = np.ones(len(c['df'][name]))*c['weights']
                    signalMC['labels'] = c['label']
                elif c['isData'] is True:
                    data['values'] = c['df'][name]
                    data['colors'] = c['color']
                    data['weights'] = np.ones(len(c['df'][name]))*c['weights']
                    data['labels'] = c['label']
                else:
                    backgroundMC['values'].append(c['df'][name])
                    backgroundMC['colors'].append(c['color'])
                    backgroundMC['weights'].append(np.ones(len(c['df'][name]))*c['weights'])
                    backgroundMC['labels'].append(c['label'])
                    totweights += c['weights']*np.sum(len(c['df'][name]))


            #print(backgroundMC)
            #print(backgroundMC['values'])
            #print(backgroundMC['weights'])
            #print(len(backgroundMC['values']))
            #print(len(backgroundMC['weights']))

            # Background
            #print(backgroundMC['colors'])
            #print(backgroundMC['labels'])
            plt.hist(backgroundMC['values'],bins=bins,range=plotrange,weights=backgroundMC['weights'],stacked=stacked,alpha=alpha,label=backgroundMC['labels'],color=backgroundMC['colors'],histtype='stepfilled',density=norm_hist)

            # Signal
            if len(signalMC['values'])>0:
                nentries = len(signalMC['values'])
                #print(f"totweights: {totweights}")
                signalMC['weights'] = np.ones(nentries)*(totweights/nentries)*0.15
                plt.hist(signalMC['values'],bins=bins,range=plotrange,weights=signalMC['weights'],lw=2,ls='--',alpha=1.0,label=signalMC['labels'],color='b',histtype='step',density=norm_hist)

            # Data
            if len(data['values'])>0:
                hist_with_errors(data['values'],bins=bins,range=plotrange,label='Data')

            if plotrange is not None:
                plt.xlim(plotrange[0],plotrange[1])

            if xlabel is not None:
                plt.xlabel(xlabel,fontsize=xlabelfontsize)
            else:
                plt.xlabel(name,fontsize=xlabelfontsize)

            #plt.legend(fontsize=8,loc='upper left')
            plt.legend(fontsize=8,loc='best')

        ########################################################################
        if i%nplots_per_figure==nplots_per_figure-1 or i==nplots-1:
            print("Here!")
            plt.tight_layout()
            filename = 'plots/stacked_cut_summary_files_{0}_{1}_{2}.png'.format(decay,tag,figcount)
            plt.savefig(filename)
            figcount += 1

        i += 1
        plt.tight_layout()
        grid_count += 1

        filename = 'plots/stacked_cut_summary_files_{0}_{1}_{2}.png'.format(decay,tag,figcount)
        plt.savefig(filename)



################################################################################
def hist_with_errors(values,bins=100,range=None,fmt='o',color='black',ecolor='black',markersize=2,axes=None,barsabove=False,capsize=0,linewidth=1,normed=False,weights=None,label=None,alpha=0.0):

    nentries_per_bin, bin_edges, patches = plt.hist(values,bins=bins,
            range=range,alpha=alpha,weights=weights) # Make histogram transparent.

    # Create an errorbar plot using the info from the histogram.
    bin_width = bin_edges[1] - bin_edges[0] # Assumes evenly spaced bins.
    xpts = bin_edges[0:-1] + bin_width/2.0 # Get the bin centers and leave off
                                           # the last point which is the high
                                           # side of a bin.

    ypts = 1.0*nentries_per_bin.copy()
    xpts_err = bin_width/2.0
    ypts_err = np.sqrt(nentries_per_bin) # Use np.sqrt to take square root
                                         # of an array. We'll assume Gaussian
                                         # errors here.
    if normed:
        ntot = float(sum(nentries_per_bin))
        ypts /= ntot
        ypts_err /= ntot


    # If no axes are passed in, use the current axes available to plt.
    if axes==None:
        axes=plt.gca()

    ret = axes.errorbar(xpts, ypts, xerr=xpts_err, yerr=ypts_err,fmt=fmt,
            color=color,ecolor=ecolor,markersize=markersize,barsabove=barsabove,capsize=capsize,
            linewidth=linewidth,label=label,alpha=1.0)

    if normed:
        axes.set_ylim(0,2.0*max(ypts))

    return ret,xpts,ypts,xpts_err,ypts_err


################################################################################
def hist2d(xvals,yvals,xbins=10,ybins=10,xrange=None,yrange=None,origin='lower',cmap=plt.cm.coolwarm,axes=None,aspect='auto',log=False,weights=None,zlim=(None,None),label=None):

    # If no ranges are passed in, use the min and max of the x- and y-vals.
    if xrange==None:
        xrange = (min(xvals),max(xvals))
    if yrange==None:
        yrange = (min(yvals),max(xvals))

    # Note I am switching the expected order of xvals and yvals, following the 
    # comment in the SciPy tutorial.
    # ``Please note that the histogram does not follow the Cartesian convention 
    # where x values are on the abcissa and y values on the ordinate axis. Rather, 
    # x is histogrammed along the first dimension of the array (vertical), and y 
    # along the second dimension of the array (horizontal). 
    # This ensures compatibility with histogramdd.
    #
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram2d.html
    H,xedges,yedges = np.histogram2d(yvals,xvals,bins=[ybins,xbins],range=[yrange,xrange],weights=weights)
    extent = [yedges[0], yedges[-1], xedges[0], xedges[-1]]

    if log is True:
        H = np.log10(H)

    # If no axes are passed in, use the current axes available to plt.
    if axes==None:
        axes=plt.gca()

    ret = axes.imshow(H,extent=extent,interpolation='nearest',origin=origin,cmap=cmap,axes=axes,aspect=aspect,vmin=zlim[0],vmax=zlim[1])
    #colorbar = plt.colorbar(cax=axes)

    return ret,xedges,yedges,H,extent

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

    decays = ['/pmu/','/pe/','/pnu/','/nmu/','/ne/']
    decays += ['_pmu_','_pe_','_pnu_','_nmu_','_ne_']

    labels = {}
    labels['1235'] = r'$B^+B^-$'
    labels['1237'] = r'$B^0\bar{B}^0$'
    labels['1005'] = r'$c\bar{c}$'
    labels['998'] = r'$u\bar{u},d\bar{d},s\bar{s}$'
    labels['3429'] = r'$\tau^+\tau^-$'
    labels['3981'] = r'$\mu^+\mu^-$'
    labels['2400'] = r'$e^+e^-$'
    labels['signal'] = r'$B\rightarrow p \ell^-$'
    labels['9456'] = r'$B\rightarrow p \mu^-$'
    labels['9457'] = r'$B\rightarrow p e^-$'
    labels['11975'] = r'$B\rightarrow p \nu$'
    labels['11976'] = r'$B\rightarrow n \mu^-$'
    labels['11977'] = r'$B\rightarrow n e^-$'
    labels['980'] = r'$B\rightarrow \pi \pi$'
    labels['Data'] = r'Data'

    tag = None
    label = None
    decay = None
    if name.find('AllEvents')>=0:
        # Data
        # basicPID_R24-AllEvents-Run1-OnPeak-R24-9_SKIMMED.root
        #tag = name.split('basicPID_R24-AllEvents-')[1].split('-OnPeak-R24-')[0]
        tag = 'All runs'
        if name.find('Run')>=0 and name.find('AllRuns')<0:
            tag = 'Run' + name.split('Run')[1][0]
        label = 'Data'
        #print("HERE!!!")
        #print(tag,label)
    elif name.find('SP')>=0:
        # MC
        index = name.find('SP')+1
        sps = ['1235', '1237', '1005', '998', '3429', '3981','2400','9456', '9457', '11975', '11976', '11977', '980']
        for sp in sps:
            if name.find(sp,index)>=index:
                break
        tag = sp
        label = labels[sp]

    for d in decays:
        if name.find(d)>=0:
            decay = d
            break

    return tag,label,decay
################################################################################
def create_df_plotting_containers(dfs,sps,labels,weights,colors):

    signalMC = ['9456','9457','11975','11976','11977']

    df_plotting_container = {}

    unique_sps = np.unique(sps).tolist()

    for sp in unique_sps:
        #print("First: ",sp)
        df_plotting_container[sp] = {'df':[], 'label':[], 'weights':[], 'color':[], 'isData':False, 'isSignalMC':False}

    for sp,df,label,weight,color in zip(sps,dfs,labels,weights,colors):
        #print("Second: ",label)
        df_plotting_container[sp]['df'].append(df)
        df_plotting_container[sp]['label'].append(label)
        df_plotting_container[sp]['weights'].append(weight)
        df_plotting_container[sp]['color'].append(color)
    
    for sp in df_plotting_container.keys():
        #print("Third: ",sp)
        dataframes = df_plotting_container[sp]['df']
        allweights = df_plotting_container[sp]['weights']
        if len(dataframes)>1:
            newdf = pd.concat(dataframes)
            print(newdf)
            print(len(newdf['bnvbcandDeltaE']))
            print(allweights)
            #newweights = np.concatenate(weights)
            # Delete them in reverse order
            for i in range(len(dataframes)-1,-1,-1):
                print(i,len(dataframes[i]['bnvbcandDeltaE']))
                #del dataframes[i]
            df_plotting_container[sp]['df'] = newdf
            df_plotting_container[sp]['weights'] = allweights[0]
        else:
            df_plotting_container[sp]['df'] = dataframes[0]
            df_plotting_container[sp]['weights'] = allweights[0]
        df_plotting_container[sp]['label'] = df_plotting_container[sp]['label'][0]
        df_plotting_container[sp]['color'] = df_plotting_container[sp]['color'][0]
        if sp in signalMC:
            df_plotting_container[sp]['isSignalMC'] = True
        if sp == 'All runs':
            df_plotting_container[sp]['isData'] = True

    #print(list(df_plotting_container.keys()))
    return df_plotting_container
