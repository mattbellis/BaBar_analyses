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
from pdf_definitions import argus_in_x,read_in_ML_output,two_argus_in_x,three_argus_in_x
import numpy as np

import sys

def main(argv):

    # Set up a workspace to store everything
    workspace_filename = "testworkspace.root"
    workspace_file = ROOT.TFile(workspace_filename, "RECREATE")

    workspace_name = "workspace_test"
    w = ROOT.RooWorkspace(workspace_name,"My workspace")

    # Set up component pdfs
    # ---------------------------------------

    # Declare observable x
    x = ROOT.RooRealVar("x", "x", 0.7, 1.0)
    x.setBins(50)
    #x.setBins(500)

    # Read in the data
    infilename = argv[1]
    #data = read_in_ML_output(infilename,x,max_vals=None)
    data = read_in_ML_output(infilename,x,max_vals=10000)


    ############################################################################
    # Create two Argus for bkg and signal
    # their parameters
    pars_bkg, argus_bkg, argus_bkg0, argus_bkg1, = two_argus_in_x(x,'bkg')
    pars_bkg[0].setVal(-3.7)
    pars_bkg[0].setRange(-100000,100000)

    pars_bkg[1].setVal(1.0)
    pars_bkg[1].setRange(0.97,1.001)

    pars_bkg[2].setVal(-73)             # par
    pars_bkg[2].setRange(-1000000,-1)
    pars_bkg[3].setVal(1.0)              # cutoff
    pars_bkg[3].setRange(0.97,1.001)

    # Fractions
    pars_bkg[4].setVal(0.7)
    pars_bkg[4].setRange(0.001,0.99)

    # Method 1 - Construct extended composite model
    # -------------------------------------------------------------------
    
    # Sum the composite bkgnal and background into an extended pdf
    # nbkg*bkg+nbkg*bkg
    nbkg = ROOT.RooRealVar("nbkg", "number of bkgnal events", 10000, 0., 1000000)
    #nbkg = ROOT.RooRealVar( "nbkg", "number of background events", 10000, 0, 1000000)
    # One argus for bkgnal
    #model = ROOT.RooAddPdf("model", "a1+a2", ROOT.RooArgList( argus_bkg, argus_bkg), ROOT.RooArgList( nbkg, nbkg))
    # Two argus for bkgnal
    #model = ROOT.RooAddPdf("model", "a1+a2", ROOT.RooArgList( argus_bkg, twoArgus_bkg), ROOT.RooArgList( nbkg, nbkg))
    model = ROOT.RooAddPdf("model", "a1", ROOT.RooArgList( argus_bkg), ROOT.RooArgList( nbkg))

    # Sample, fit and plot extended model

    # Fit model to data, ML term automatically included
    results = model.fitTo(data,ROOT.RooFit.Save(ROOT.kTRUE))

    # Plot data and PDF overlaid, expected number of events for p.d.f projection normalization
    # rather than observed number of events (==data.numEntries())
    xframe = x.frame(ROOT.RooFit.Title("extended ML fit example"))
    data.plotOn(xframe)
    model.plotOn(xframe, ROOT.RooFit.Normalization( 1.0, ROOT.RooAbsReal.RelativeExpected))

    # Overlay the background component of model with a dashed line
    '''
    ras_bkg = ROOT.RooArgSet(argus_bkg)
    model.plotOn(
        xframe, ROOT.RooFit.Components(ras_bkg), ROOT.RooFit.LineStyle(
            ROOT.kDashed), ROOT.RooFit.Normalization(
                1.0, ROOT.RooAbsReal.RelativeExpected))
    '''

    # Overlay the background+bkg2 components of model with a dotted line
    ras_bkg0 = ROOT.RooArgSet(argus_bkg0)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_bkg0), 
                         ROOT.RooFit.LineStyle(ROOT.kDotted), 
                         ROOT.RooFit.LineColor(ROOT.kRed), 
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         ) 

    ras_bkg1 = ROOT.RooArgSet(argus_bkg1)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_bkg1), 
                         ROOT.RooFit.LineStyle(ROOT.kDotted), 
                         ROOT.RooFit.LineColor(ROOT.kRed), 
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         ) 

    # Print structure of composite p.d.f.
    model.Print("t")

    # Draw the frame on the canvas
    c = ROOT.TCanvas("fit", "fit", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    #xframe.SetAxisRange(0.98,1.0,"X")
    xframe.Draw()
    #xframe.SetMaximum(10000)
    ROOT.gPad.Update()
    c.SaveAs("fit_to_data.png")

    # Draw the frame on the canvas
    c1 = ROOT.TCanvas("fit1", "fit1", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    xframe.SetAxisRange(0.98,1.0,"X")
    xframe.Draw()
    #xframe.SetMaximum(10000)
    ROOT.gPad.Update()
    c1.SaveAs("fit_to_data1.png")

    print("Print the results -------------------------")
    results.Print("v")

    ############################################################################
    # Save the workspace
    # This needs to be first, before its subcomponent PDF's
    getattr(w,'import')(model)
    #getattr(w,'import')(twoArgus_sig)
    getattr(w,'import')(data)

    # Save the fit results.
    results.SetName("testname_results")
    getattr(w,'import')(results)

    print("Print the contents of the workspace -------------------------")
    w.Print()

    workspace_file.cd()
    w.Write()
    workspace_file.Close()
    ############################################################################



    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

################################################################################
if __name__ == '__main__':
    main(sys.argv)


