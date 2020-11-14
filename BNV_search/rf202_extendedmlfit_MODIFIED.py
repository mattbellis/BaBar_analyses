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

def main():
    # Set up component pdfs
    # ---------------------------------------

    # Declare observable x
    x = ROOT.RooRealVar("x", "x", 0.5, 1.0)
    x.setBins(25)

    # Create two Gaussian PDFs g1(x,mean1,sigma) anf g2(x,mean2,sigma) and
    # their parameters
    pars_bkg, argus_bkg = argus_in_x(x,'bkg')
    pars_bkg[0].setVal(1)
    pars_bkg[1].setVal(0.98)

    pars_sig, argus_sig = argus_in_x(x,'sig')
    pars_sig[0].setVal(-7)
    pars_sig[1].setVal(0.98)


    # Method 1 - Construct extended composite model
    # -------------------------------------------------------------------
    
    # Sum the composite signal and background into an extended pdf
    # nsig*sig+nbkg*bkg
    nsig = ROOT.RooRealVar("nsig", "number of signal events", 100, 0., 10000)
    nbkg = ROOT.RooRealVar( "nbkg", "number of background events", 300, 0, 10000)
    model = ROOT.RooAddPdf("model", "a1+a2",
        ROOT.RooArgList( argus_bkg, argus_sig), ROOT.RooArgList( nbkg, nsig))

    # Sample, fit and plot extended model
    # ---------------------------------------------------------------------
    
    # Generate a data sample of expected number events in x from model
    # = model.expectedEvents() = nsig+nbkg
    data = model.generate(ROOT.RooArgSet(x))

    # Fit model to data, ML term automatically included
    model.fitTo(data)

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

    c.SaveAs("rf202_extendedmlfit.png")

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

################################################################################
if __name__ == '__main__':
    main()


