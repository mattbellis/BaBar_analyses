## \file
## \ingroup tutorial_roofit
## \notebook
## Addition and convolution: setting up an extended maximum likelihood fit
##
## \macro_code
##
## \date February 2018
## \author Clemens Lange, Wouter Verkerke (C++ version)

import ROOT
from pdf_definitions import argus_in_x
import numpy as np

import sys

def main(argv):
    # Set up component pdfs
    # ---------------------------------------


    # Declare observable x
    x = ROOT.RooRealVar("x", "x", 0.7, 1.0)
    x.setBins(100)

    # Create two Gaussian PDFs g1(x,mean1,sigma) anf g2(x,mean2,sigma) and
    # their parameters
    pars_bkg, argus_bkg = argus_in_x(x,'bkg')
    pars_bkg[0].setVal(-100.0) # Negative means peak at high values, positive means peak at low values
    pars_bkg[0].setRange(-100000,100000)

    pars_bkg[1].setVal(1.0) # This is the cutoff, how high in x the PDF can go
    pars_bkg[1].setRange(0.01,100000.001)

    pars_sig, argus_sig = argus_in_x(x,'sig')
    pars_sig[0].setVal(-500) # Negative means peak at high values, positive means peak at low values
    pars_sig[0].setRange(-5000000,5000000)

    pars_sig[1].setVal(1.0) # This is the cutoff, how high in x the PDF can go
    pars_sig[1].setRange(0.97,1.001)


    # Method 1 - Construct extended composite model
    # -------------------------------------------------------------------
    
    # Sum the composite signal and background into an extended pdf
    # nsig*sig+nbkg*bkg
    #nsig = ROOT.RooRealVar("nsig", "number of signal events", 100000, 0., 1000000)
    #nbkg = ROOT.RooRealVar( "nbkg", "number of background events", 300, 0, 1000000)

    nsig = ROOT.RooRealVar("nsig", "number of signal events", 30000, 0., 1000000)
    nbkg = ROOT.RooRealVar( "nbkg", "number of background events", 10000, 0, 1000000)
    model = ROOT.RooAddPdf("model", "a1+a2",
        ROOT.RooArgList( argus_bkg, argus_sig), ROOT.RooArgList( nbkg, nsig))

    # Sample, fit and plot extended model
    # ---------------------------------------------------------------------
    
    # Generate a data sample of expected number events in x from model
    # = model.expectedEvents() = nsig+nbkg
    data = model.generate(ROOT.RooArgSet(x))
    

    # Plot data and PDF overlaid, expected number of events for p.d.f projection normalization
    # rather than observed number of events (==data.numEntries())
    xframe = x.frame(ROOT.RooFit.Title("extended ML fit example"))
    data.plotOn(xframe)
    model.plotOn(xframe, ROOT.RooFit.Normalization( 1.0, ROOT.RooAbsReal.RelativeExpected))

    # Overlay the background component of model with a dashed line
    ras_bkg = ROOT.RooArgSet(argus_bkg)
    model.plotOn(
        xframe, ROOT.RooFit.Components(ras_bkg), ROOT.RooFit.LineStyle(
            ROOT.kDashed), ROOT.RooFit.Normalization(
                1.0, ROOT.RooAbsReal.RelativeExpected))

    # Overlay the background+sig2 components of model with a dotted line
    ras_bkg_sig2 = ROOT.RooArgSet(argus_sig)
    model.plotOn(
                xframe, ROOT.RooFit.Components(ras_bkg_sig2), ROOT.RooFit.LineStyle(
                            ROOT.kDotted), ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.Normalization(
                                            1.0, ROOT.RooAbsReal.RelativeExpected))


    # Print structure of composite p.d.f.
    model.Print("t")

    bkgvalue0 = pars_bkg[0].getVal()
    bkgvalue1 = pars_bkg[1].getVal()
    bkgvalue2 = nbkg.getVal()
    txt = ROOT.TText(0.5,0.8,f"bkg: {bkgvalue0:0.2f}  {bkgvalue1:0.2f}   {bkgvalue2}") 
    txt.SetNDC()
    txt.SetTextSize(0.04)
    xframe.addObject(txt)

    sigvalue0 = pars_sig[0].getVal()
    sigvalue1 = pars_sig[1].getVal()
    sigvalue2 = nsig.getVal()
    txt = ROOT.TText(0.5,0.7,f"sig: {sigvalue0:0.2f}  {sigvalue1:0.2f}   {sigvalue2}") 
    txt.SetNDC()
    txt.SetTextSize(0.04)
    xframe.addObject(txt)

    #value = pars_bkg[1].getVal()
    #txt = ROOT.TText(0.6,0.75,f"bkg 1: {value:0.2f}") 
    #txt.SetNDC()
    #xframe.addObject(txt)
#
    #value = pars_sig[0].getVal()
    #txt = ROOT.TText(0.6,0.7,f"sig 0: {value:0.2f}") 
    #txt.SetNDC()
    #xframe.addObject(txt)
#
    #value = pars_sig[1].getVal()
    #txt = ROOT.TText(0.6,0.65,f"sig 1: {value:0.2f}") 
    #txt.SetNDC()
    #xframe.addObject(txt)
#



    # Method 2 - Construct extended components first
    # ---------------------------------------------------------------------
    
    # Associated nsig/nbkg as expected number of events with sig/bkg
    esig = ROOT.RooExtendPdf("esig", "extended signal p.d.f", argus_sig, nsig)
    ebkg = ROOT.RooExtendPdf("ebkg", "extended background p.d.f", argus_bkg, nbkg)

    # Sum extended components without coefs
    # -------------------------------------------------------------------------
     
    # Construct sum of two extended p.d.f. (no coefficients required)
    model2 = ROOT.RooAddPdf("model2", "(g1+g2)+a", ROOT.RooArgList(ebkg, esig))

    # Draw the frame on the canvas
    c = ROOT.TCanvas("rf202_extendedmlfit", "rf202_extendedmlfit", 600, 600)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    xframe.Draw()
    ROOT.gPad.Update()

    name = f"RooFit_functions_sig_{sigvalue0:0.2f}_{sigvalue1:0.2f}_{sigvalue2:0.2f}_bkg_{bkgvalue0:0.2f}_{bkgvalue1:0.2f}_{bkgvalue2:0.2f}.png"
    c.SaveAs(name)

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

################################################################################
if __name__ == '__main__':
    main(sys.argv)


