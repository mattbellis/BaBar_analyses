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
from pdf_definitions import crystal_barrel_x
import numpy as np
import plotting_tools as pt

import sys
import os

def main(argv):

    infilename = argv[1]
    print(f"Processing file...{infilename}")
    tag,label,decay = pt.get_sptag(infilename)
    print(tag,label,decay)
    # Decay probably is something like _ne_ so remove the underscores
    #decay = decay[1:-1]
    if decay is None and infilename.find('pmu')>=0:
        decay = 'pmu'
    elif decay is None and infilename.find('pe')>=0:
        decay = 'pe'
    else:
        decay = "DEFAULT"
    print(tag,label,decay)


    # Set up a workspace to store everything
    #workspace_filename = "testworkspace.root"
    workspace_filename = f"workspace_{infilename.split('.')[0]}.root"
    workspace_file = ROOT.TFile(workspace_filename, "RECREATE")

    workspace_name = "workspace"
    w = ROOT.RooWorkspace(workspace_name,"My workspace")

    # Set up component pdfs
    # ---------------------------------------

    # Declare observable x
    #x = ROOT.RooRealVar("x", "x", 0.7, 1.0)
    x = ROOT.RooRealVar("x", "x", 5.2, 5.3)
    x.setBins(10)
    #x.setBins(50)
    #x.setBins(200)

    # Read in the data
    #data = read_in_ML_output(infilename,x,max_vals=None)
    data = read_in_ML_output(infilename,x,max_vals=10000)


    ############################################################################
    # Create an Argus function for background and its
    # their parameters
    pars_bkg, twoArgus, argus_bkg0, argus_bkg1 = two_argus_in_x(x,'bkg')

    pars_bkg[0].setVal(-20)
    pars_bkg[0].setRange(-80,0)

    pars_bkg[1].setVal(5.29)
    pars_bkg[1].setRange(5.2, 5.3)

    pars_bkg[2].setVal(-200)
    pars_bkg[2].setRange(-1000,-85)

    pars_bkg[3].setVal(5.29)
    pars_bkg[3].setRange(5.2, 5.3)

    pars_bkg[4].setVal(0.9)
    pars_bkg[4].setRange(0.0, 1.0)

    # Method 1 - Construct extended composite model
    # -------------------------------------------------------------------
    
    # Sum the composite signal and background into an extended pdf
    # nsig*sig+nbkg*bkg
    nbkg = ROOT.RooRealVar("nbkg", "number of background events", 10000, 0., 1000000)
    model = ROOT.RooAddPdf("model_bkg", "a1", ROOT.RooArgList(twoArgus), ROOT.RooArgList( nbkg))
    #model = arg_bkg

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

    # Overlay the background+sig2 components of model with a dotted line
    ras_bkg0 = ROOT.RooArgSet(argus_bkg0)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_bkg0), 
                         ROOT.RooFit.LineStyle(ROOT.kDotted), 
                         ROOT.RooFit.LineColor(ROOT.kBlue), 
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         ) 

    ras_bkg1 = ROOT.RooArgSet(argus_bkg1)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_bkg1), 
                         ROOT.RooFit.LineStyle(ROOT.kDotted), 
                         ROOT.RooFit.LineColor(ROOT.kBlue), 
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         ) 

    '''
    # One argus for sig
    ras_bkg_sig2 = ROOT.RooArgSet(argus_sig)
    model.plotOn(
                xframe, ROOT.RooFit.Components(ras_bkg_sig2), ROOT.RooFit.LineStyle(
                            ROOT.kDotted), ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.Normalization(
                                            1.0, ROOT.RooAbsReal.RelativeExpected))
    '''

    '''
    # Two argus for sig
    ras_sig2 = ROOT.RooArgSet(twoArgus_sig,argus0_sig,argus1_sig)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_sig2), 
                         ROOT.RooFit.LineStyle(ROOT.kDotted), 
                         ROOT.RooFit.LineColor(ROOT.kRed), 
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         ) 
    ras_sig3 = ROOT.RooArgSet(argus0_sig)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_sig3), 
                         ROOT.RooFit.LineStyle(ROOT.kDotted), 
                         ROOT.RooFit.LineColor(ROOT.kRed), 
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         ) 
    ras_sig4 = ROOT.RooArgSet(argus1_sig)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_sig4), 
                         ROOT.RooFit.LineStyle(ROOT.kDotted), 
                         ROOT.RooFit.LineColor(ROOT.kRed), 
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         )

    '''
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
    ''' # Zoomed maybe
    c1 = ROOT.TCanvas("fit1", "fit1", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    #xframe.SetAxisRange(0.98,1.0,"X")
    xframe.SetAxisRange(5.2,5.3,"X")
    xframe.Draw()
    #xframe.SetMaximum(10000)
    ROOT.gPad.Update()
    #c1.SaveAs("fit_to_data1.png")
    c1.SaveAs(f"{outdir}/fit_to_data_ZOOM_{infilename}.png")
    '''


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

################################################################################
if __name__ == '__main__':
    main(sys.argv)


