import uproot
import awkward as ak

import pandas as pd

import matplotlib.pylab as plt
import numpy as np

import hist
from hist import Hist

import time

import myPIDselector

import math

import os

################################################################################
def read_in_dataset_statistics(infilename='dataset_statistics.csv'):
    df = pd.read_csv(infilename)

    return df
################################################################################

################################################################################
def get_SP_cross_sections_and_labels(infilename='SP_cross_sections_and_labels.csv'):
    df = pd.read_csv(infilename)

    return df
################################################################################

################################################################################
def create_table_of_data_skims_statistics():
    df = read_in_dataset_statistics()
    
    dfspinfo = get_SP_cross_sections_and_labels()

    mask = dfspinfo['SP Mode']==1235
    bbbar_xsec = dfspinfo[mask]['Cross section [nb]'].values[0]

    mask = dfspinfo['SP Mode']==1237
    bbbar_xsec += dfspinfo[mask]['Cross section [nb]'].values[0]

    print(f"The total BBbar cross section is {bbbar_xsec} nb")

    mask = df['Data or MC']=='Data'
    #df[mask]

    mask = (df['Data or MC']=='Data') & (df['Skim']=='LambdaVeryVeryLoose')
    dftmp = df[mask][['Run', 'Luminosity (Data only) 1/pb','# of events (Data or MC)', '# of events (Data or MC) NOT SURE WHICH NUMBER TO USE']]

    dftmp['# of BBbar pairs'] = dftmp['Luminosity (Data only) 1/pb']*bbbar_xsec*1000

    dftmp['Run'] = dftmp['Run'].astype(int).astype(str)
    dftmp.loc['Total'] = dftmp.sum(numeric_only=True)

    dftmp.at['Total','Run'] = 'Total'

    header = []
    header.append('Run')
    header.append('Luminosity (1/pb)')
    header.append('\# skimmed events')
    header.append('\# org. events')
    header.append('\# BB pairs')

    caption = "Details of the numbers of events and luminosity from the {\\tt LambdaVeryVeryLoose} skim used in this analysis."
    label = 'tab:dataskims'

    df.style.to_latex(position_float='centering')

    output = dftmp.to_latex(index=False, header=header, float_format="%.1f", caption=caption, label=label)

    # Add in centering by replacing the first EOL with "EOL + \centering + EOL"
    output = output.replace('\n','\n\centering\n', 1)

    # Add an hline learn the bottom above the total
    output = output.replace('Total','\hline\nTotal', 1)

    return output


################################################################################

###################################################################################
def calculate_bits_for_PID_selector(trkidx, trk_selector_map, verbose=0):
    
    bits = None

    # If there is no trk index passed in, just calculate the bits for
    # all of the tracks
    if trkidx is None:
        trkidx = ak.local_index(trk_selector_map)

    # Grab the tracks that map on to the particle/collection we are interested in 
    subset_of_trk_selector_map = trk_selector_map[trkidx]
    if verbose:
        print("values in the subset of the trk selector map")
        print(subset_of_trk_selector_map)
        print()
        
    # We need this to convert the numbers in the selector to binary
    binary_repr_vec = np.vectorize(np.binary_repr)

    # Grab the number of entries in each so we can unflatten this later
    counts = ak.num(subset_of_trk_selector_map)
    
    # Now get the binary representation (as a string) for the flattened subset
    binrep = binary_repr_vec(ak.flatten(subset_of_trk_selector_map), width=32)

    if verbose:
        print("binary representation of selector map")
        print(binrep)
        print()

    # Convert the string to integers
    tempbits = np.array(binrep).astype(int)
    bits = ak.unflatten(tempbits,counts)

    if verbose:
        print("flattened integer representation of selectors as binary (int)")
        print(tempbits)
        print()
        print("unflattened integer representation of selectors as binary (int)")
        print(bits)
        print()

    return bits

##########################################################################

##########################################################################

def mask_PID_selection(bits, selector, pid_map_object):

    bit_to_look_for = pid_map_object.selectors.index(selector)

    place = int(math.pow(10,bit_to_look_for))
    #print(place)

    mask = bits // place % 10

    mask_bool = ak.values_astype(mask,bool)

    return mask_bool


##########################################################################
def scaling_value(spmode, dataset_information=None, cs_data=None, plot= False, verbose= False):
    mode= spmode 

    if spmode==0 or spmode==-999:
        return 1 # This is data
    
    mc_mask= (dataset_information["SP mode"]== mode) & (dataset_information["Skim"] != "LambdaVeryVeryLoose")
    # Pulls out all unskimmed MC with desired SP mode
    
    nevents_mc= dataset_information[mc_mask]["# of events (Data or MC)"].sum()
    # Sums the number of unskimmed MC events of the desired SP mode
                
    cs_mask= cs_data["SP Mode"]== mode

    cs= cs_data[cs_mask]["Cross section [nb]"]

    cs= cs.values[0]

    mask = (dataset_information['Data or MC'] == 'Data') & (dataset_information['Skim'] != 'LambdaVeryVeryLoose')
    int_lumi = dataset_information[mask]['Luminosity (Data only) 1/pb'].sum()
    
    n_exp_in_data= cs* int_lumi*1000 
    # Factor of 1000 arises from multiplying nanobarnes by 1/picobarnes
    
    scaling= n_exp_in_data/nevents_mc
    # MC is intentionally overgenerated, so to figure out how to weight the MC, divide the number generated by the total number of MC events

    
    if plot== True:
        spmask = data['spmode']== str(mode)
        x = data[spmask]['BpostFitMes'][:,0]
        plt.hist(x,bins=100, range=(5., 5.3), weights=scaling*np.ones(len(x)));
        plt.title(f"Scaling value for SP-{mode}: {scaling:.4f}")

    if verbose== True: 
        print(f"- Cross section for this SP mode is    {cs} nb")
        print(f"- # of events generated for SP-{mode}: {nevents_mc:13d}")
        print(f"- Number expected in data:             {n_exp_in_data:.1f}")
        print(f"- Integrated Luminosity:               {int_lumi:.1f} 1/pb")
        print("The scaling value for this SP mode is: ")

    return scaling

##########################################################################

def table_from_df(df, outfilename):
    output = df.to_latex(index=False,
                  float_format="{:.4f}".format,
    )  # converts dataframe into latex readable text
    full_table = "\\begin{table}\n" # initializes the table before the beginning of the tabular 
    full_table += "\\caption{This could be the caption}\n" 
    full_table += output #includes the converted dataframe in the table
    full_table += "\\end{table}" # ends the table, same purpose as begin{table} 
    filename= f"table_{outfilename}.tex"
    path= f"tables/{filename}"
    outfile = open(path, 'w')
    outfile.write(full_table)
    outfile.close()    
    return print(full_table) #make sure to return the print() of the full_table, otherwise it'll be one big string that latex can't handle


##########################################################################

def indices_to_booleans(indices, array_to_slice):
    whole_set, in_set = ak.unzip(ak.cartesian([ 
                                  ak.local_index(array_to_slice), indices ], nested=True))

    return ak.any(whole_set == in_set, axis=-1)

##########################################################################

def build_antiproton_antimask(data, pps, selector = 'SuperLooseKMProtonSelection', IS_MC=True, verbose=0):

    if verbose:
        print("The MC and tracks for the first entry")
        idx = data['TRKMCIdx'][0]
        if IS_MC:
            mclund = data['mcLund'][0]

            for i,id in enumerate(idx):
                print(f"{i:2d}  {id:4d}   {mclund[id]}")
            print()

    
    lamd1idx = data['Lambda0d1Idx']
    lamd1Lund = data['Lambda0d1Lund']

    if verbose:
        print(f'lamd1idx\n{lamd1idx}')
        print(f'lamd1Lund\n{lamd1Lund}')
    
    d2idx = data['Bd2Idx']
    d2Lund = data['Bd2Lund']

    if verbose:
        print()
        print(f'B d2idx\n{d2idx}')
        print(f'B d2Lund\n{d2Lund}')
        print()

    qBd2 = (data['Bd2Lund'])/np.abs(data['Bd2Lund'])
    print(qBd2)
    print(qBd2[:,0])
    qBd2 = qBd2[:,0]

    qlamd1 = (data['Lambda0d1Lund'])/np.abs(data['Lambda0d1Lund'])
    qlamd1 = qlamd1[:,0]

    if verbose:
        print("Proton charges ----------------")
        print(f"qBd2\n{qBd2}\n")
        print(f"qlamd1\n{qlamd1}\n")
        print("Proton charges ----------------\n\n")

    qtrk = (data['TRKLund'])/np.abs(data['TRKLund'])

    if verbose:
        print("Track charges ----------------")
        print(f"qtrk\n{qtrk}\n")
        print("Track charges ----------------\n\n")
    
    
    trkidx_proton = data['pTrkIdx']

    if verbose:
        print(f"# of protons: {data['np']}")
        print(f"trkidx_proton (the track index for labeled protons) \n{trkidx_proton}")
        print()
    
    lamd1_trkidx = trkidx_proton[lamd1idx]
    d2_trkidx = trkidx_proton[d2idx]

    if verbose:
        print(f"lamd1_trkidx\n{lamd1_trkidx}\n")    
        print(f"B d2_trkidx\n{d2_trkidx}\n")
    

    trk_selector_map = data['pSelectorsMap']
    
    if verbose:
        print(f"qtrk\n{qtrk}\n")
        print(f"proton trk_selector_map\n{trk_selector_map}\n")
        print(f"pion   trk_selector_map\n{data['piSelectorsMap']}\n")
        print(f"kaon   trk_selector_map\n{data['KSelectorsMap']}\n")

    lamproton_selector_map = trk_selector_map[lamd1_trkidx]

    if verbose:
        print(lamproton_selector_map)
        print()
    
    bool_idx1 = indices_to_booleans(lamd1_trkidx, trk_selector_map)
    bool_idx2 = indices_to_booleans(d2_trkidx, trk_selector_map)

    if verbose:
        print(f"proton track selectors for the index of the proton from the lambda (and not that)")
        print(f"The boolean mask bool_idx1\n{bool_idx1}")
        print(trk_selector_map[bool_idx1])
        print(trk_selector_map[~bool_idx1])
        print()

        print(f"proton track selectors for the index of the proton from the B (and not that)")
        print(f"The boolean mask bool_idx1\n{bool_idx2}")
        print(trk_selector_map[bool_idx2])
        print(trk_selector_map[~bool_idx2])
        print()
        
    
        # Both protons
        print(f"Boolean for both protons (or) \n{(bool_idx1 | bool_idx2)}")
        print(f"trk selectors for both protons (or) \n{trk_selector_map[bool_idx1 | bool_idx2]}")
        print(f"trk selectors for other protons     \n{trk_selector_map[~(bool_idx1 | bool_idx2)]}")
        print()
    
    
    
    pbits = calculate_bits_for_PID_selector(None, trk_selector_map)

    if verbose:
        print(f"The pbits -----------------")
        print(f'All the pbits\n{pbits}')
        print(f"bool for protons from Lambda\n{bool_idx1}")
        print(f'pbits for protons from Lambda     pbits[bool_idx1]\n{pbits[bool_idx1]}')
        print(f'pbits for protons not from Lambda pbits[~bool_idx1]\n{pbits[~bool_idx1]}')
        print()

        print(f"bool for protons from B\n{bool_idx2}")
        print(f'pbits for protons from B     pbits[bool_idx2]\n{pbits[bool_idx2]}')
        print(f'pbits for protons not from B pbits[~bool_idx2]\n{pbits[~bool_idx2]}')
        print()

        
    mask_bool = mask_PID_selection(pbits, selector, pps)

    if verbose:
        print(f"mask_bool, (mask_PID_selection) the tracks that pass {selector}")
        print(mask_bool)
        print(pbits[mask_bool])
        print(pbits[~mask_bool])
        print()
        
        print(f"pbits that are not the final state lambda but are protons")
        print(pbits[~bool_idx1 & mask_bool])
        print()
        
        print(f"TRKcharge that are not the final state lambda but are protons")
        print(qtrk[~bool_idx1 & mask_bool])
        print()
    
    charge_test_idx1 = qtrk[~bool_idx1 & mask_bool] == -qlamd1
    charge_test_idx2 = qtrk[~bool_idx2 & mask_bool] == -qBd2

    if verbose:
        print(f"charge test idx1\n{charge_test_idx1}")
        print(f"charge test idx2\n{charge_test_idx2}")
    

    # This is True if there is an antiproton in the other final state particles
    # This is likely (I think) with background and less likely with signal
    charge_test = qtrk[~(bool_idx1 | bool_idx2) & mask_bool] == -qlamd1

    if verbose:
        print(f"charge test both: is neither Lam/B dau, passes selectors, opposite charge\n{charge_test}")

    if verbose:
        print("\nCounting..............")
        print(f'{charge_test[charge_test] = }')
        print(f'{ak.num(charge_test[charge_test]) = }')
        print(f'{ak.sum(ak.num(charge_test[charge_test])) = }')
        print()
    
    #nhave_opposite = ak.sum(ak.num(charge_test[charge_test]))
    #n = ak.num(charge_test, axis=0)
    
    have_opp = ak.num(charge_test[charge_test])
    
    nhave_opp = len(have_opp[have_opp>0])

    ndont_have_opp = len(have_opp[have_opp==0])

    n = len(data)

    if verbose:
        print(f"# of events:                                  {n}")
        print(f"# of events that don't have opposite protons: {ndont_have_opp}")
        print(f"# of events that       have opposite protons: {nhave_opp}")

    # Select events that *don't* have opposite protons
    mask_no_antiprotons = ak.any(charge_test, axis=-1)

    return mask_no_antiprotons, charge_test

################################################################################
def create_empty_histograms(hist_defs): 
    ### Creates empty Hist object histograms based on the information in the dictionary above
    ### Then overwrites the information in the dictionary to be the hist object. All_hists goes from containing unconnected
    ### info about each variable to a single object containing all the same info 
    
    all_hists={}
    for var in hist_defs.keys():
        h = Hist.new.Reg(hist_defs[var]["nbins"], hist_defs[var]["lo"], hist_defs[var]["hi"], name='var', label=f"{hist_defs[var]['label']}") \
                 .StrCat([], name="SP", label="SP modes", growth=True)\
                 .StrCat([], name="cuts", label="Cuts", growth=True)\
                 .Weight()
    
        all_hists[var] = h

    return all_hists



################################################################################
def fill_histograms_v2(ak_arr, empty_hists, spmodes=['998'], weights=[1.0]):
    ### Takes the dictionary of objects we made before and fills them 
    ### with the correct information, based on SP mode and Cut. 
    ### Each cut pares down the background and hopefully makes the signal more apparent

    # Save the result of the cuts in a dataframe
    df_dict = {}
    df_dict['var'] = []
    df_dict['cut'] = []
    df_dict['spmode'] = []
    df_dict['n'] = []

    for key in empty_hists.keys(): 
        print(key)

        for spmode in spmodes:
            #print(spmode)
            weight = 1
            if spmode=='-999':
                weight = .005
            else:
                weight = weights[spmode]

            all_cuts = {}
            mask_sp= (ak_arr.spmode== spmode)            
            mask_fl0 = (ak_arr['Lambda0FlightLen']>=0)
            mask_fl1 = (ak_arr['Lambda0FlightLen']>=1)
            mask_ntrk = (ak_arr['nTRK'] > 4)

            # Blinding
            mes = ak_arr['BpostFitMes']
            de  = ak_arr['BpostFitDeltaE']           
            # Stuff
            blinding_mask =   (mes>5.27) & ((de>-.07) & (de<.07)) 
            fitarea_mask   =  (mes>5.2) & ((de>-.2) & (de<.2)) 

            #var_mask = mask_fl & ~blinding_mask & fitarea_mask

            all_cuts['0'] = {'mask_ev':mask_sp, 'mask_part':mask_fl0}
            all_cuts['1'] = {'mask_ev':mask_sp & mask_ntrk, 'mask_part':mask_fl0}
            all_cuts['2'] = {'mask_ev':mask_sp & mask_ntrk, 'mask_part':mask_fl1}
            all_cuts['3'] = {'mask_ev':mask_sp & mask_ntrk, 'mask_part':mask_fl1 & ~blinding_mask & fitarea_mask}
            all_cuts['4'] = {'mask_ev':mask_sp & mask_ntrk, 'mask_part':mask_fl1 & fitarea_mask}

            for cutname,cutmasks in all_cuts.items():

                #print(f"cutname: {cutname}")

                mask_ev =   cutmasks['mask_ev']
                mask_part = cutmasks['mask_part']

                n = -1
                # Apply the cuts and fill the histograms
                if key[0]=='B' or key.find('Lambda0')==0:
                    x = ak.flatten(ak_arr[mask_ev][key][mask_part[mask_ev]])
                else:
                    x = ak_arr[mask_ev][key]

                n = len(x)
                empty_hists[key].fill(var=x, SP= spmode, cuts= f"{cutname}", weight= weight)

                # Fill the dataframe dictionary
                df_dict['var'].append(key)
                df_dict['cut'].append(cutname)
                df_dict['spmode'].append(spmode)
                df_dict['n'].append(n)

    df = pd.DataFrame.from_dict(df_dict)
    
    return df

def plot_histograms(all_hists, vars=[], bkg_spmodes=['998'], datamodes=['0'], sig_spmodes=['-999'], cut='0', save= True, overlay_data=True, only_stacked=False, fixed_grid=None):
    
    ### makes a directory (if it doesn't already exist) for these plots.
    ### plots will be saved to this dictionary if save= true
    current_dir= os.getcwd()
    directory = "BNV_pLambda_plots"
    path= os.path.join(current_dir,directory)
    if os.path.isdir(path)== False:
        os.mkdir(path)
    
    if len(vars) == 0:
        vars = list(all_hists.keys())

    ### color scheme dictionary
    cd= {}
    cd["998"]=  {"tab:blue"}
    cd["1005"]= {"tab:orange"}
    cd["-999"]= {"tab:brown"}
    cd["1235"]= {"tab:green"}
    cd["1237"]= {"tab:red"}
    cd["3981"]= {"tab:purple"}
    cd["3429"]= {"tab:pink"}
    cd["0"]= {"tab:cyan"}

    print(bkg_spmodes)

    if only_stacked and fixed_grid:
        width = fixed_grid[0] * 5
        height = fixed_grid[1] * 3
        plt.figure(figsize=(width,height))           

    
    for axes_idx,var in enumerate(vars):
        
        h = all_hists[var]
                
        if only_stacked and not fixed_grid:   # if you only want the stacked sp and not the breakdown for individual modes 
            plt.figure(figsize=(5,3))
        elif only_stacked and fixed_grid:     # fixed grid is a grid of subplots 
            plt.subplot(fixed_grid[0], fixed_grid[1], axes_idx+1)
        else:
            plt.figure(figsize=(18,12))
            plt.subplot(3,3,1)
            
        h[:,bkg_spmodes,cut].stack('SP')[:].project('var').plot(stack=True, histtype="fill")
        h[:,sig_spmodes,cut].project('var').plot(histtype="step", color='yellow', label= "signal")

        if overlay_data:
            h[:,datamodes,cut].project('var').plot(histtype="errorbar", color='black', label='Data')

        plt.legend()
        plt.xlabel(plt.gca().get_xlabel(), fontsize=18)


        # If we are only plotting the stacked histograms, then we can skip over plotting them individually
        if not only_stacked:
            
            # Plot all the others 
            all_modes = bkg_spmodes + sig_spmodes + datamodes
            
            for idx,spmode in enumerate(all_modes):
                plt.subplot(3,3,idx+2)
                h[:,spmode,cut].project('var').plot(histtype="fill", label=spmode, color= cd[str(spmode)])
                plt.legend()
                plt.xlabel(plt.gca().get_xlabel(), fontsize=18)

        plt.tight_layout()
        
        if save== True:
            
            outfilename=f"plot_hist_cut{cut}_{var}.png" 
            if only_stacked and not fixed_grid:
                outfilename=f"plot_hist_cut{cut}_ONLY_STACKED_{var}.png" 
                
            plt.savefig(f"{path}/{outfilename}")

    if save== True and fixed_grid and only_stacked:
        # name of .png saved to computer based on fields specified on function call 
        varnames = "_".join(vars)
        outfilename=f"plot_hist_cut{cut}_ONLY_STACKED_FIXED_GRID_{varnames}.png" 
            
        plt.savefig(f"{path}/{outfilename}")
################################################################################

################################################################################
def get_signal_mask(data, region_definitions):
    mes= data["BpostFitMes"]
    de= data["BpostFitDeltaE"]
    signal_mask = (mes > region_definitions["signal MES"][0]) & ((de>region_definitions["signal DeltaE"][0]) & (de<region_definitions["signal DeltaE"][1])) 
    #fitarea_mask   =  (mes>5.2) & ((de>-.2) & (de<.2))
    return signal_mask 

################################################################################

################################################################################
def get_fit_mask(data, region_definitions):
    mes= data["BpostFitMes"]
    de= data["BpostFitDeltaE"]
    fit_mask = (mes > region_definitions["fitting MES"][0]) & ((de>region_definitions["fitting DeltaE"][0]) & (de<region_definitions["fitting DeltaE"][1])) 
    return fit_mask 

################################################################################
################################################################################
def get_flight_len_mask(data, region_definitions, flightlenvar='Lambda0FlightLen'):
    
    cutvariable = data[flightlenvar]

    mask_fl = cutvariable>region_definitions['Lambda0 flightlen']

    lo = region_definitions['Lambda0 mass'][0]
    hi = region_definitions['Lambda0 mass'][1]

    m = data['Lambda0_unc_Mass']
    mask = (m>lo) & (m<hi) & mask_fl

    return mask

################################################################################


################################################################################
def get_duplicates_mask(data):

    fl = data['Lambda0FlightLen']

    # Cuts out duplicates
    mask_fl = fl>=0

    # Keep events with only 1 B candidate
    nB = ak.num(data['BMass'][mask_fl])
    
    mask = nB==1

    return mask, mask_fl

################################################################################

def PID_masks(data, \
              lamp_selector='VeryLooseKMProtonSelection', \
              lampi_selector='SuperLooseKMPionMicroSelection', \
              Bp_selector='VeryLooseKMProtonSelection', \
             verbosity=0):
    # Get these maps first
    pps = myPIDselector.PIDselector("p")
    pips = myPIDselector.PIDselector("pi")

    if verbosity:
        print("Names of selectors:\npions")
        print(pips.selectors)
        print("\nprotons\n")
        print(pps.selectors) 

    # Proton and pion information from the Lambda decay
    # These are the index of the proton (d1) and pion (d2) in those lists
    d1idx = data['Lambda0d1Idx']
    d2idx = data['Lambda0d2Idx']
    
    d1lund = data['Lambda0d1Lund']
    d2lund = data['Lambda0d2Lund']
    
    Bd2idx = data['Bd2Idx']
    Bd2lund = data['Bd2Lund']

    if verbosity==1:
        print(d1lund)
        print(d2lund)
        print(Bd2lund)
        print()
        
        print(d1idx)
        print(d2idx)
        print(Bd2idx)
        print()
    
    trkidx_proton = data['pTrkIdx']
    trk_selector_map_proton = data['pSelectorsMap']
    
    trkidx_pion = data['piTrkIdx']
    trk_selector_map_pion = data['piSelectorsMap']
    
    # Proton
    pbits = calculate_bits_for_PID_selector(trkidx_proton, trk_selector_map_proton, verbose=verbosity)
    # Pion
    pibits = calculate_bits_for_PID_selector(trkidx_pion, trk_selector_map_pion, verbose=verbosity)
    
    
    #selector_proton = 'TightKMProtonSelection'
    #selector_pion = 'TightKMPionMicroSelection'
    #print(f"Now trying to create a mask with {selector_proton}")
    #print(f"Now trying to create a mask with {selector_pion}")
    
    
    mask_bool_proton = mask_PID_selection(pbits[d1idx], lamp_selector, pps)
    mask_bool_protonB = mask_PID_selection(pbits[Bd2idx], Bp_selector, pps)
        
    mask_bool_pion = mask_PID_selection(pibits[d2idx], lampi_selector, pips)

    return mask_bool_proton, mask_bool_pion, mask_bool_protonB


##########################################################################




##########################################################################
def plot_mes_vs_DeltaE(mes, DeltaE, draw_signal_region=False, tag=None, region_definitions=None, bins=100):

    meslo = region_definitions['fitting MES'][0]
    meshi = region_definitions['fitting MES'][1]

    h= Hist(
    hist.axis.Regular(bins,meslo,meshi,name= "sig_BPFM", label= "M$_{ES}$ [GeV/c$^2$]", flow= True),
    hist.axis.Regular(bins,-.5,.5,name= "bkg_BPFMDE", label= "$\Delta$E [GeV]", flow= True),
    )

    # normal fill
    h.fill(mes, DeltaE)

    h.plot2d_full(
            #main_cmap="coolwarm",
        main_cmap="plasma",
        top_ls="--",
        top_color="orange",
        top_lw=2,
        side_ls=":",
        side_lw=2,
        side_color="steelblue",
    )

    #plt.xlim(5.1,5.3)
    #plt.ylim(-.5,.5)
    #plt.show()


    #'''
    if draw_signal_region==True:
        plt.plot([5.2002,5.2002,5.3,5.3,5.2],[-0.2,0.2,0.2,-0.2,-0.2], "w-", linewidth= 4)
        plt.plot([5.27,5.27,5.29,5.29,5.27],[-0.07,0.07,0.07,-0.07,-0.07], "k--", linewidth= 4)
    #'''

    plt.xlabel(plt.gca().get_xlabel(), fontsize=18)
    plt.ylabel(plt.gca().get_ylabel(), fontsize=18)
    plt.tight_layout()

    if tag is not None:
        plt.savefig(f'BNV_pLambda_plots/plot_{tag}_bkg_de_vs_mes.png')



##########################################################################
