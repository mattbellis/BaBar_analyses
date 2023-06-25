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
from pdf_definitions import argus_in_x,read_in_ML_output,two_argus_in_x,three_argus_in_x,two_argus_plus_expon_in_x
import numpy as np

import plotting_tools as pt

import sys
import os

def main(argv):

    infilename = argv[1]
    print(f"Processing file...{infilename}")
    tag,label,decay = pt.get_sptag(infilename)
    # Decay probably is something like _ne_ so remove the underscores
    decay = decay[1:-1]
    print(tag,label,decay)

    # Set up a workspace to store everything
    #workspace_filename = "testworkspacebkg.root"
    workspace_filename = f"workspace_{infilename}.root"
    workspace_file = ROOT.TFile(workspace_filename, "RECREATE")

    workspace_name = "workspace"
    w = ROOT.RooWorkspace(workspace_name,"My workspace")

    # Set up component pdfs
    # ---------------------------------------

    # Declare observable x
    #x = ROOT.RooRealVar("x", "x", 0.7, 1.0)
    x = ROOT.RooRealVar("x", "x", 0.2, 1.0)
    x.setBins(50)
    #x.setBins(500)

    # Read in the data
    #data = read_in_ML_output(infilename,x,max_vals=None)
    #data = read_in_ML_output(infilename,x,max_vals=10000)
    data = read_in_ML_output(infilename,x,max_vals=20000)


    ############################################################################
    # Create two Argus for bkg and signal
    # their parameters
    #pars_bkg, argus_bkg, argus_bkg0, argus_bkg1, = two_argus_in_x(x,'bkg')
    pars_bkg, twoArgusPlusExp, argus_bkg0, argus_bkg1, expon = two_argus_plus_expon_in_x(x,'bkg')
    pars_bkg[0].setVal(-3.7) # par
    pars_bkg[0].setRange(-100000,100000)

    pars_bkg[1].setVal(1.0) # cutoff
    pars_bkg[1].setRange(0.97,1.001)

    pars_bkg[2].setVal(-73)             # par
    pars_bkg[2].setRange(-1000000,-1)

    pars_bkg[3].setVal(1.0)              # cutoff
    pars_bkg[3].setRange(0.97,1.001)

    pars_bkg[4].setVal(-2.0)              # exp slope
    pars_bkg[4].setRange(-10,-0.1)

    # Fractions
    pars_bkg[5].setVal(0.3)
    pars_bkg[5].setRange(0.001,0.99)

    pars_bkg[5].setVal(0.4)
    pars_bkg[5].setRange(0.001,0.99)


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
    model = ROOT.RooAddPdf("model_bkg", "a1", ROOT.RooArgList( twoArgusPlusExp), ROOT.RooArgList( nbkg))

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

    ras_bkg2 = ROOT.RooArgSet(expon)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_bkg2), 
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

    outdir = f'plots_{decay}'
    if not os.path.exists(outdir):
       os.makedirs(outdir)

    c.SaveAs(f"{outdir}/fit_to_data_{infilename}.png")

    # Draw the frame on the canvas
    c1 = ROOT.TCanvas("fit1", "fit1", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    #xframe.SetAxisRange(0.98,1.0,"X")
    xframe.SetAxisRange(0.90,1.0,"X")
    xframe.SetAxisRange(0.00,70.0,"Y")
    xframe.Draw()
    #xframe.SetMaximum(10000)
    ROOT.gPad.Update()
    c1.SaveAs(f"{outdir}/fit_to_data_ZOOM_{infilename}.png")

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


    if len(argv)<=2 or argv[2].find('batch')<0:
        rep = ''
        while not rep in [ 'q', 'Q' ]:
            rep = input( 'enter "q" to quit: ' )
            if 1 < len(rep):
                rep = rep[0]

    return 1

################################################################################
if __name__ == '__main__':
    ret = main(sys.argv)


