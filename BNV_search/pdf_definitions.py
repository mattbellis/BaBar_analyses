#!/usr/bin/env python

import numpy as np
import ROOT 

################################################################################
# Read in the data and return a RooDataset
################################################################################
def read_in_ML_output(infilename,x=None,max_vals=None):

    original_data = np.load(infilename)

    print(original_data)
    print(f"min/max: {max(original_data)} {min(original_data)}")

    data = ROOT.RooDataSet("data","data",ROOT.RooArgSet(x))
    xlo = x.getRange()[0]
    xhi = x.getRange()[1]
    print(f"Ranges for data: {xlo} - {xhi}")

    for i,d in enumerate(original_data):

        if max_vals is not None and i>=max_vals:
            break

        #print(d)
        if i%100000==0:
            print(i,len(original_data))
        if i>1000000:
            break
        if d>xlo and d<xhi:
            x.setVal(d)
            data.add(ROOT.RooArgSet(x))

    return data

################################################################################


###############################################################
# Background and signal definition
###############################################################

################################################################################
# Argus background PDF
################################################################################
def argus_in_x(x,tag='default'):
    argpar = ROOT.RooRealVar("argpar_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff = ROOT.RooRealVar("cutoff_"+tag,"Argus cutoff "+tag,5.29,-1000,1000)

    argus = ROOT.RooArgusBG("argus_"+tag,"Argus PDF "+tag,x,cutoff,argpar)

    pars = [argpar, cutoff]
    return pars, argus 
################################################################################

################################################################################
# Two Argus
################################################################################
def two_argus_in_x(x,tag='default'):
    argpar0 = ROOT.RooRealVar("argpar0_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff0 = ROOT.RooRealVar("cutoff0_"+tag,"Argus cutoff "+tag,1.00,-1000,1000)
    argus0 = ROOT.RooArgusBG("argus0_"+tag,"Argus PDF "+tag,x,cutoff0,argpar0)

    argpar1 = ROOT.RooRealVar("argpar1_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff1 = ROOT.RooRealVar("cutoff1_"+tag,"Argus cutoff "+tag,1.00,-1000,1000)
    argus1 = ROOT.RooArgusBG("argus1_"+tag,"Argus PDF "+tag,x,cutoff1,argpar1)

    frac_two_argus = ROOT.RooRealVar("argus_frac_"+tag,"Two Argus fraction "+tag,0.50,0,1.0)

    twoArgus = ROOT.RooAddPdf(
    "twoArgus_"+tag, "Two Argus functions "+tag, ROOT.RooArgList(argus0, argus1), ROOT.RooArgList(frac_two_argus))

    pars = [argpar0, cutoff0, argpar1, cutoff1, frac_two_argus]

    return pars, twoArgus, argus0, argus1
################################################################################

################################################################################
# Three Argus
################################################################################
def three_argus_in_x(x,tag='default'):
    argpar0 = ROOT.RooRealVar("argpar0_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff0 = ROOT.RooRealVar("cutoff0_"+tag,"Argus cutoff "+tag,1.00,-1000,1000)
    argus0 = ROOT.RooArgusBG("argus0_"+tag,"Argus PDF "+tag,x,cutoff0,argpar0)

    argpar1 = ROOT.RooRealVar("argpar1_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff1 = ROOT.RooRealVar("cutoff1_"+tag,"Argus cutoff "+tag,1.00,-1000,1000)
    argus1 = ROOT.RooArgusBG("argus1_"+tag,"Argus PDF "+tag,x,cutoff1,argpar1)

    argpar2 = ROOT.RooRealVar("argpar2_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff2 = ROOT.RooRealVar("cutoff2_"+tag,"Argus cutoff "+tag,1.00,-1000,1000)
    argus2 = ROOT.RooArgusBG("argus2_"+tag,"Argus PDF "+tag,x,cutoff2,argpar2)

    frac_three_argus0 = ROOT.RooRealVar("argus_frac0_"+tag,"Two Argus fraction 0 "+tag,0.50,0,1.0)
    frac_three_argus1 = ROOT.RooRealVar("argus_frac1_"+tag,"Two Argus fraction 1 "+tag,0.50,0,1.0)

    threeArgus = ROOT.RooAddPdf(
    "threeArgus_"+tag, "Three Argus functions "+tag, ROOT.RooArgList(argus0, argus1, argus2), ROOT.RooArgList(frac_three_argus0,frac_three_argus1))

    pars = [argpar0, cutoff0, argpar1, cutoff1, argpar2, cutoff2, frac_three_argus0, frac_three_argus1]

    return pars, threeArgus, argus0, argus1, argus2
################################################################################

################################################################################
# Two Argus + exponential
################################################################################
def two_argus_plus_expon_in_x(x,tag='default'):
    argpar0 = ROOT.RooRealVar("argpar0_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff0 = ROOT.RooRealVar("cutoff0_"+tag,"Argus cutoff "+tag,1.00,-1000,1000)
    argus0 = ROOT.RooArgusBG("argus0_"+tag,"Argus PDF "+tag,x,cutoff0,argpar0)

    argpar1 = ROOT.RooRealVar("argpar1_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff1 = ROOT.RooRealVar("cutoff1_"+tag,"Argus cutoff "+tag,1.00,-1000,1000)
    argus1 = ROOT.RooArgusBG("argus1_"+tag,"Argus PDF "+tag,x,cutoff1,argpar1)

    expslope = ROOT.RooRealVar("expslope_"+tag,"Exponential slope "+tag,-10.0,-100,-0.1)
    expon = ROOT.RooExponential("expon_"+tag,"Exponential PDF "+tag,x,expslope)

    frac_two_argus_plus_expon0 = ROOT.RooRealVar("argus_frac_plus_expon0_"+tag,"Two Argus + expon fraction 0 "+tag,0.50,0,1.0)
    frac_two_argus_plus_expon1 = ROOT.RooRealVar("argus_frac_plus_expon1_"+tag,"Two Argus + expon fraction 1 "+tag,0.50,0,1.0)

    twoArgusPlusExp = ROOT.RooAddPdf(
    "twoArgusPlusExp_"+tag, "Two Argus functions + exponential "+tag, ROOT.RooArgList(argus0, argus1, expon), ROOT.RooArgList(frac_two_argus_plus_expon0, frac_two_argus_plus_expon1))

    pars = [argpar0, cutoff0, argpar1, cutoff1, expslope, frac_two_argus_plus_expon0, frac_two_argus_plus_expon1 ]

    return pars, twoArgusPlusExp, argus0, argus1, expon
################################################################################

