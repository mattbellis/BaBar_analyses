import uproot
import awkward as ak

import matplotlib.pylab as plt
import numpy as np

import hist
from hist import Hist

import time

import myPIDselector

import math


###################################################################################
def calculate_bits_for_PID_selector(trkidx, trk_selector_map, verbose=0):
    
    bits = None

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

def table_from_df(df):
    output = df.to_latex(index=False,
                  float_format="{:.4f}".format,
    )  # converts dataframe into latex readable text
    full_table = "\\begin{table}\n" # initializes the table before the beginning of the tabular 
    full_table += "\\caption{This could be the caption}\n" 
    full_table += output #includes the converted dataframe in the table
    full_table += "\\end{table}" # ends the table, same purpose as begin{table} 
    return print(full_table) #make sure to return the print() of the full_table, otherwise it'll be one big string that latex can't handle

##########################################################################
