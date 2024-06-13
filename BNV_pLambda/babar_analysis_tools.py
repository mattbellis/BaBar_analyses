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
