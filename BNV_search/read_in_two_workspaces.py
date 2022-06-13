import ROOT
import numpy as np

import sys

def main(argv):

    constraint_multiplier = 0.2

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

    #exit()

    model_bkg = w.pdf("model_bkg");
    nbkg = w.var("nbkg");

    nsig.setVal(1000)
    nbkg.setVal(29000)


    model = ROOT.RooAddPdf("model","n1*a1 + n2*a2",ROOT.RooArgList(model_sig, model_bkg), ROOT.RooArgList(nsig, nbkg))

    '''
    data = model.generate(ROOT.RooArgSet(x),nsig.getVal() + nbkg.getVal())
    model.fitTo(data)


    xframe = x.frame(ROOT.RooFit.Title("extended ML fit example"))

    data.plotOn(xframe)
    model.plotOn(xframe, ROOT.RooFit.Normalization( 1.0, ROOT.RooAbsReal.RelativeExpected))


    c1 = ROOT.TCanvas("fit1", "fit1", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    #xframe.SetAxisRange(0.95,1.0,"X")
    xframe.Draw()
    ROOT.gPad.Update()
    '''
    #mcstudy = ROOT.RooMCStudy(model, ROOT.RooArgSet(x), ROOT.RooFit.Binned(ROOT.kTRUE), ROOT.RooFit.Silence(), ROOT.RooFit.Extended(), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.PrintEvalErrors(0)));
    mcstudy = ROOT.RooMCStudy(model, ROOT.RooArgSet(x), ROOT.RooFit.Binned(ROOT.kTRUE), ROOT.RooFit.Verbose(ROOT.kTRUE) , ROOT.RooFit.Extended(), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.PrintEvalErrors(1), ROOT.RooFit.Verbose(ROOT.kTRUE)));
    #mcstudy = ROOT.RooMCStudy(model, ROOT.RooArgSet(x), ROOT.RooFit.Extended(), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.PrintEvalErrors(0)));

    genData = model.generate(x,30000) 
    genData.Print()
    model.fitTo(genData, ROOT.RooFit.FitOptions(ROOT.RooFit.Binned(ROOT.kTRUE)))
    xframe = x.frame()
    genData.plotOn(xframe)
    model.plotOn(xframe, ROOT.RooFit.Normalization( 1.0, ROOT.RooAbsReal.RelativeExpected))
    xframe.Draw()
    #exit()

    # A trials of B events each trial
    mcstudy.generateAndFit(1000,30000)

    # Make plots of the distributions of nsig, the error on nsig and the pull of nsig
    frame1 = mcstudy.plotParam(nsig, ROOT.RooFit.Bins(40));
    frame2 = mcstudy.plotError(nsig, ROOT.RooFit.Bins(40));
    frame3 = mcstudy.plotPull(nsig, ROOT.RooFit.Bins(40), ROOT.RooFit.FitGauss(ROOT.kTRUE));

    frame5 = mcstudy.plotParam(nbkg, ROOT.RooFit.Bins(40));

    # Plot distribution of minimized likelihood
    frame4 = mcstudy.plotNLL(ROOT.RooFit.Bins(40));

    # Make some histograms from the parameter dataset
    hh_cor_a0_s1f = mcstudy.fitParDataSet().createHistogram( nsig, nbkg, "", "hh")
    #hh_cor_a0_s1f = mcstudy.fitParDataSet().createHistogram("hh", nsig, ROOT.RooFit.YVar(nbkg));
    #hh_cor_a0_a1 = mcstudy.fitParDataSet().createHistogram("hh", a0, ROOT.RooFit.YVar(a1));

    # Access some of the saved fit results from individual toys
    corrHist000 = mcstudy.fitResult(0).correlationHist("c000");
    #corrHist127 = mcstudy.fitResult(127).correlationHist("c127");
    #corrHist953 = mcstudy.fitResult(953).correlationHist("c953");

    # Draw all plots on a canvas
    #gStyle->SetOptStat(0);
    c = ROOT.TCanvas("rf801_mcstudy", "rf801_mcstudy", 900, 900);
    c.Divide(3, 3);
    c.cd(1);
    ROOT.gPad.SetLeftMargin(0.15);
    frame1.GetYaxis().SetTitleOffset(1.4);
    frame1.Draw();
    c.cd(2);
    ROOT.gPad.SetLeftMargin(0.15);
    frame2.GetYaxis().SetTitleOffset(1.4);
    frame2.Draw();

    c.cd(3);
    ROOT.gPad.SetLeftMargin(0.15);
    frame3.GetYaxis().SetTitleOffset(1.4);
    frame3.Draw();

    c.cd(4);
    ROOT.gPad.SetLeftMargin(0.15);
    frame4.GetYaxis().SetTitleOffset(1.4);
    frame4.Draw();
    c.cd(5);
    ROOT.gPad.SetLeftMargin(0.15);
    hh_cor_a0_s1f.GetYaxis().SetTitleOffset(1.4);
    hh_cor_a0_s1f.Draw("box");
    #c.cd(6);
    #ROOT.gPad.SetLeftMargin(0.15);
    #hh_cor_a0_a1.GetYaxis().SetTitleOffset(1.4);
    #hh_cor_a0_a1.Draw("box");
    c.cd(7);
    ROOT.gPad.SetLeftMargin(0.15);
    corrHist000.GetYaxis().SetTitleOffset(1.4);
    corrHist000.Draw("colz");

    c.cd(9);
    ROOT.gPad.SetLeftMargin(0.15);
    frame5.GetYaxis().SetTitleOffset(1.4);
    frame5.Draw();
    '''
    c.cd(8);
    ROOT.gPad.SetLeftMargin(0.15);
    corrHist127.GetYaxis().SetTitleOffset(1.4);
    corrHist127.Draw("colz");
    c.cd(9);
    ROOT.gPad.SetLeftMargin(0.15);
    corrHist953.GetYaxis().SetTitleOffset(1.4);
    corrHist953.Draw("colz");
    '''
    ROOT.gPad.Update()




    ########################;
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]


################################################################################
if __name__ == '__main__':
    main(sys.argv)




