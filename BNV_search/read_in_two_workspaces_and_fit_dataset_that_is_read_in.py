import ROOT
import numpy as np

import sys

from pdf_definitions import read_in_ML_output
from pdf_definitions import argus_in_x,read_in_ML_output,two_argus_in_x,three_argus_in_x
from pdf_definitions import argus_in_x,read_in_ML_output,two_argus_in_x,three_argus_in_x,two_argus_plus_expon_in_x



def main(argv):

    constraint_multiplier = 0.2
    nentries = 30000
    nsiginit = 1000
    ntrials = 20

    # Set up a workspace to store everything
    #workspace_filename = "testworkspace.root"
    print("Read in signal.............")
    workspace_filename = argv[1]
    workspace_file = ROOT.TFile(workspace_filename)
    workspace_file.Print()
    workspace_file.ls()
    w = workspace_file.Get("workspace")
    w.Print()
    variable_dict = {}
    #print(w)
    for v in w.allVars():
        print(v)
        name = v.GetName()
        val = v.getVal()
        err = v.getError()
        variable_dict[name] = [val,err]
        if name is not 'x' and name[0]!='n':
            #v.setConstant(ROOT.kTRUE)
            # Or
            v.setRange(val-(constraint_multiplier*err),val+(constraint_multiplier*err))

    x = w.var("x");
    x.setRange(0.2,1.0) # Just for nmu for now
    x.setBins(50)
    model_sig = w.pdf("model_sig");
    nsig = w.var("nsig");

    print("Read in background.............")
    workspace_filename = argv[2]
    workspace_file = ROOT.TFile(workspace_filename)
    workspace_file.Print()
    workspace_file.ls()
    w = workspace_file.Get("workspace")
    w.Print()
    #print(w)
    for v in w.allVars():
        print(v)
        name = v.GetName()
        val = v.getVal()
        err = v.getError()
        variable_dict[name] = [val,err]
        if name is not 'x' and name[0]!='n':
            #v.setConstant(ROOT.kTRUE)
            # Or
            v.setRange(val-(constraint_multiplier*err),val+(constraint_multiplier*err))
    print(variable_dict)

    ############################################################################
    infilename = argv[3]

    x = ROOT.RooRealVar("x", "x", 0.2, 1.0)
    #x.setBins(50)
    x.setBins(200)

    # Read in the data
    #data = read_in_ML_output(infilename,x,max_vals=None)
    data = read_in_ML_output(infilename,x,max_vals=1000000)
    ############################################################################


    #exit()

    model_bkg = w.pdf("model_bkg");
    nbkg = w.var("nbkg");

    nsig.setVal(nsiginit)
    nsig.setRange(1,nentries)
    nbkg.setVal(nentries-nsiginit)
    nbkg.setRange(0,nentries)


    model = ROOT.RooAddPdf("model","n1*a1 + n2*a2",ROOT.RooArgList(model_sig, model_bkg), ROOT.RooArgList(nsig, nbkg))

    #results = model.fitTo(data,ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.RooCmdArg(SetMaxCalls))
    nll = model.createNLL(data);
    m = ROOT.RooMinimizer(nll)
    # Activate verbose logging of MINUIT parameter space stepping
    m.setVerbose(ROOT.kTRUE);
    # Call MIGRAD to minimize the likelihood
    m.migrad();
    results = m.save();
    
    xframe = x.frame(ROOT.RooFit.Title("extended ML fit example"))
    data.plotOn(xframe)
    model.plotOn(xframe, ROOT.RooFit.Normalization( 1.0, ROOT.RooAbsReal.RelativeExpected))

	# Overlay the background+sig2 components of model with a dotted line
    pars_sig, argus_sig, argus_sig0, argus_sig1, argus_sig2 = three_argus_in_x(x,'sig')
    pars_bkg, twoArgusPlusExp, argus_bkg0, argus_bkg1, expon = two_argus_plus_expon_in_x(x,'bkg')


    ras_sig0 = ROOT.RooArgSet(argus_sig0)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_sig0),
                         ROOT.RooFit.LineStyle(ROOT.kDotted),
                         ROOT.RooFit.LineColor(ROOT.kBlue),
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         )

    ras_sig1 = ROOT.RooArgSet(argus_sig1)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_sig1),
                         ROOT.RooFit.LineStyle(ROOT.kDotted),
                         ROOT.RooFit.LineColor(ROOT.kBlue),
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         )

    ras_sig2 = ROOT.RooArgSet(argus_sig2)
    model.plotOn(xframe, ROOT.RooFit.Components(ras_sig2),
                         ROOT.RooFit.LineStyle(ROOT.kDotted),
                         ROOT.RooFit.LineColor(ROOT.kBlue),
                         ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                         )

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
    #c.SaveAs("fit_to_data.png")
    c.SaveAs(f"fit_to_data_{infilename}.png")


    # Draw the frame on the canvas
    c1 = ROOT.TCanvas("fit1", "fit1", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    #xframe.SetAxisRange(0.98,1.0,"X")
    xframe.SetAxisRange(0.90,1.0,"X")
    #xframe.SetAxisRange(0.0,10.0,"Y")
    xframe.Draw()
    #xframe.SetMaximum(10000)
    ROOT.gPad.Update()
    #c1.SaveAs("fit_to_data1.png")
    c1.SaveAs(f"fit_to_data_ZOOM_{infilename}.png")


    # NLL scan
    #'''
    framescan = nsig.frame(ROOT.RooFit.Bins(10),ROOT.RooFit.Range(1,200),ROOT.RooFit.Title("LL and profileLL in nsig"))
    nll.plotOn(framescan,ROOT.RooFit.ShiftToZero()) 

    pll_frac = nll.createProfile(ROOT.RooArgSet(nsig)) ;
    # Plot the profile likelihood in frac
    pll_frac.plotOn(framescan,ROOT.RooFit.LineColor(ROOT.kRed)) ;

    c2 = ROOT.TCanvas("scan", "scan", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    framescan.GetYaxis().SetTitleOffset(1.4)
    #framescan.SetAxisRange(0.98,1.0,"X")
    #framescan.SetAxisRange(0.90,1.0,"X")
    framescan.Draw()
    #framescan.SetMaximum(10000)
    ROOT.gPad.Update()
    c2.SaveAs(f"fit_to_data_NLL_scan_{infilename}.png")
    #'''


    ROOT.gPad.Update()

    print("Print the results -------------------------")
    results.Print("v")



    ########################;
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

    return results,framescan,pll_frac

################################################################################
if __name__ == '__main__':
    results = main(sys.argv)




