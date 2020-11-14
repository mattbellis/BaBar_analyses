#!/usr/bin/env python

import ROOT 

###############################################################
# Background and signal definition
###############################################################

################################################################################
# Argus background PDF
################################################################################
def argus_in_x(x,tag='default'):
    argpar = ROOT.RooRealVar("argpar_"+tag,"Argus shape par "+tag,-20.0)
    cutoff = ROOT.RooRealVar("cutoff_"+tag,"Argus cutoff "+tag,5.29)

    argus = ROOT.RooArgusBG("argus_"+tag,"Argus PDF "+tag,x,cutoff,argpar)

    pars = [argpar, cutoff]
    return pars, argus 
################################################################################

