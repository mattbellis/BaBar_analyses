#!/usr/bin/env python

import ROOT 

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
    argus0 = ROOT.RooArgusBG("argus_"+tag,"Argus PDF "+tag,x,cutoff0,argpar0)

    argpar1 = ROOT.RooRealVar("argpar1_"+tag,"Argus shape par "+tag,-20.0,-1000,10000)
    cutoff1 = ROOT.RooRealVar("cutoff1_"+tag,"Argus cutoff "+tag,1.00,-1000,1000)
    argus1 = ROOT.RooArgusBG("argus_"+tag,"Argus PDF "+tag,x,cutoff1,argpar1)

    frac_two_argus = ROOT.RooRealVar("argus_frac_"+tag,"Two Argus fraction "+tag,0.50,0,1.0)

    twoArgus = ROOT.RooAddPdf(
    "twoArgus_"+tag, "Two Argus functions "+tag, ROOT.RooArgList(argus0, argus1), ROOT.RooArgList(frac_two_argus))

    pars = [argpar0, cutoff0, argpar1, cutoff1, frac]

    return pars, twoArgus, argus0, argus1
################################################################################

