import numpy as np
import ROOT

import sys

import zipfile

import matplotlib.pylab as plt
import pickle


################################################################################
# Plotting utility
################################################################################
#'''
def display_histogram(h,xlabel='xlabel',ylabel='ylabel',ax=None,xfontsize=12,yfontsize=12,label=None):

    if ax is not None:
        plt.sca(ax)
    
    #print(len(h[1][:-1]), len(h[0]), h[1][1]-h[1][0])
    plt.bar(h[1][:-1], h[0], width=h[1][1]-h[1][0],label=label)
    plt.gca().set_xlabel(xlabel,fontsize=xfontsize)
    plt.gca().set_ylabel(ylabel,fontsize=yfontsize)

#'''
