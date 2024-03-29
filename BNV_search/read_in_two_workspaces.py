################################################################################
# Read in two workspaces and run some MC studies with them. 
################################################################################
import ROOT
import numpy as np

import sys
import os

import plotting_tools as pt

from pdf_definitions import argus_in_x,read_in_ML_output,two_argus_in_x,three_argus_in_x
from pdf_definitions import argus_in_x,read_in_ML_output,two_argus_in_x,three_argus_in_x,two_argus_plus_expon_in_x


def main(argv):

    workspace_filename1 = argv[1]
    workspace_filename2 = argv[2]
    nsiginit = int(argv[3])
    ntrials = int(argv[4])
    usertag = argv[5]

    fit_once = False
    if ntrials<0:
        fit_once = True

    result = -1
    mcstudy = -1

    print(f"Processing files...{workspace_filename1}")
    print(f"Processing files...{workspace_filename2}")
    tag,label,decay = pt.get_sptag(workspace_filename2)
    print(tag,label,decay)
    # Decay probably is something like _ne_ so remove the underscores
    #decay = decay[1:-1]
    #
    if workspace_filename1.find('pmu')>=0:
        decay = 'pmu'
    elif workspace_filename1.find('pe')>=0:
        decay = 'pe'
    elif workspace_filename1.find('pnu')>=0:
        decay = 'pnu'
    elif workspace_filename1.find('_ne')>=0:
        decay = 'ne'
    elif workspace_filename1.find('nmu')>=0:
        decay = 'nmu'
    else:
        decay = "DEFAULT"

    print(tag,label,decay)
    outdir = f"plots_{decay}"
    #exit()

    constraint_multiplier = 0.2
    nentries = 80000 # nmu
    if decay=='nmu':
        nentries = 80000 # nmu
    elif decay=='ne':
        nentries = 30000 # ne
    elif decay=='pnu':
        nentries = 30000 # pnu
    elif decay=='pmu':
        nentries = 400 # pmu
    elif decay=='pe':
        nentries = 120 # pe


    ############################################################################
    # Set up a workspace to store everything
    #workspace_filename = "testworkspacebkg.root"
    #workspace_outfilename = f"workspace_TRIALS_FROM_TWO_WORKSPACES_{n1}_{n2}.root"
    #binned_tag = "BINNED"
    binned_tag = "NOTBINNED"
    tag = f"{decay}_{usertag}_{binned_tag}_nsig_{nsiginit}_ntrials_{ntrials}_{np.random.randint(1,1000000000):010d}"
    #workspace_outfilename = f"workspace_TRIALS_FROM_TWO_WORKSPACES_{decay}_{binned_tag}_nsig_{nsiginit}_ntrials_{ntrials}_{np.random.randint(1,1000000000):010d}.root"
    workspace_outfilename = f"workspace_TRIALS_FROM_TWO_WORKSPACES_{tag}.root"
    workspace_outfile = ROOT.TFile(workspace_outfilename, "RECREATE")

    workspace_outname = "workspace_trials"
    wout = ROOT.RooWorkspace(workspace_outname,"My workspace")
    ############################################################################


    # Set up a workspace to store everything
    #workspace_filename = "testworkspace.root"
    print("Read in signal.............")
    workspace_file = ROOT.TFile(workspace_filename1)
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
        if name != 'x' and name[0]!='n':
            #v.setConstant(ROOT.kTRUE)
            # Or
            v.setRange(val-(constraint_multiplier*err),val+(constraint_multiplier*err))

        # Lock down the shape parameters for the signal
        if name[0]!='n' and name.find('sig'):
            v.setRange(val-(0.001*err),val+(0.001*err))

    x = w.var("x");
    if decay=='pmu' or decay=='pe':
        x.setRange(5.2,5.3) # For the mES fits
    else:
        x.setRange(0.2,1.0) # For the neural net fits

    x.setBins(50)
    model_sig = w.pdf("model_sig");
    nsig = w.var("nsig");

    print("Read in background.............")
    workspace_file = ROOT.TFile(workspace_filename2)
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
        if name != 'x' and name[0]!='n':
            #v.setConstant(ROOT.kTRUE)
            # Or
            v.setRange(val-(constraint_multiplier*err),val+(constraint_multiplier*err))
    print(variable_dict)

    #exit()

    model_bkg = w.pdf("model_bkg");
    nbkg = w.var("nbkg");

    nsig.setVal(nsiginit)
    nsig.setRange(1,nentries)
    nbkg.setVal(nentries-nsiginit)
    nbkg.setRange(0,nentries)


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

    # Binned to make it faster
    if binned_tag == "BINNED":
        mcstudy = ROOT.RooMCStudy(model, ROOT.RooArgSet(x), ROOT.RooFit.Binned(ROOT.kTRUE), ROOT.RooFit.Verbose(ROOT.kTRUE) , ROOT.RooFit.Extended(), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.PrintEvalErrors(1), ROOT.RooFit.Verbose(ROOT.kTRUE)));
    else:
        # Not binned
        mcstudy = ROOT.RooMCStudy(model, ROOT.RooArgSet(x),                                 ROOT.RooFit.Verbose(ROOT.kTRUE) , ROOT.RooFit.Extended(), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.PrintEvalErrors(1), ROOT.RooFit.Verbose(ROOT.kTRUE)));
    #mcstudy = ROOT.RooMCStudy(model, ROOT.RooArgSet(x), ROOT.RooFit.Extended(), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.PrintEvalErrors(0)));
    print("\nInitialized the RooMCStudy object....\n")

    if fit_once:

        genData = model.generate(x,nentries) 
        genData.Print()

        #model.fitTo(genData, ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.FitOptions(ROOT.RooFit.Binned(ROOT.kTRUE)))
        result = model.fitTo(genData, ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.FitOptions(ROOT.RooFit.Binned(ROOT.kTRUE)))
        result.Print()

        #'''
        init = result.floatParsInit()
        final = result.floatParsFinal()
        for i in range(len(init)):
            print(f"{init[i].GetName():16s}   {init[i].getVal():14.6f}   {final[i].getVal():14.6f}")
        #'''


        #exit()

        c1 = ROOT.TCanvas("c1", "c1", 900, 500);
        c1.Divide(1, 1);
        c1.cd(1);
        ROOT.gPad.SetLeftMargin(0.15);

        xframe = x.frame()

        genData.plotOn(xframe)

        model.plotOn(xframe, ROOT.RooFit.Normalization( 1.0, ROOT.RooAbsReal.RelativeExpected))

        # Overlay the background+sig2 components of model with a dotted line
        pars_sig, argus_sig, argus_sig0, argus_sig1, argus_sig2 = three_argus_in_x(x,'sig')
        pars_bkg, twoArgusPlusExp, argus_bkg0, argus_bkg1, expon = two_argus_plus_expon_in_x(x,'bkg')

        ras_sig_tot = ROOT.RooArgSet(argus_sig)
        model.plotOn(xframe, ROOT.RooFit.Components(ras_sig_tot),
                             ROOT.RooFit.LineColor(ROOT.kBlue),
                             ROOT.RooFit.Normalization(1.0, ROOT.RooAbsReal.RelativeExpected)
                             )

        ras_sig1 = ROOT.RooArgSet(argus_sig1)
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


        xframe.Draw()
        ROOT.gPad.Update()
        c1.SaveAs(f'{outdir}/mc_study_fit_once_{tag}.png')
        #exit()

    else:
        # A trials of B events each trial
        mcstudy.generateAndFit(ntrials,nentries)#, ROOT.kTRUE)

        print("mcstudy.genParDataSet()")
        print(mcstudy.genParDataSet())

        # More info on how the number of generated events varies
        # https://root-forum.cern.ch/t/roomcstudy-pull-calculation-and-getting-generated-values-of-parameters/37359

        ############################################################################
        # Dump the results
        # https://root.cern/doc/v606/classRooMCStudy.html
        #status = 0    : OK
        #status = 1    : Covariance was mad  epos defined
        #status = 2    : Hesse is invalid
        #status = 3    : Edm is above max
        #status = 4    : Reached call limit
        #status = 5    : Any other failure
        # https://root-forum.cern.ch/t/meaning-of-values-returned-by-roofitresult-status/16355
        #
        # Some of these are failing because they reach the call limit. However, we don't seem to be able to
        # access that direcly in MCStudy
        # We can change this by using fitTo()
        # https://root-forum.cern.ch/t/changing-minimizer-options-in-rooabspdf-fitto/18358
        nsuccessful_fits = 0
        for i in range(ntrials):
            result = mcstudy.fitResult(i)
            print(result.status(), result.numInvalidNLL())
            if result.status()==0:
                nsuccessful_fits += 1
            # These are the final fit parameters
            '''
            params = mcstudy.fitParams(0)
            for p in params:
                print(p)
            '''
        ############################################################################

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

        # Draw all plots on a canvas
        #gStyle->SetOptStat(0);
        c1 = ROOT.TCanvas("c1", "c1", 900, 300);
        c1.Divide(3, 1);
        c1.cd(1);
        ROOT.gPad.SetLeftMargin(0.15);
        frame1.GetYaxis().SetTitleOffset(1.4);
        frame1.Draw();

        c1.cd(2);
        ROOT.gPad.SetLeftMargin(0.15);
        frame2.GetYaxis().SetTitleOffset(1.4);
        frame2.Draw();

        c1.cd(3);
        ROOT.gPad.SetLeftMargin(0.15);
        frame3.GetYaxis().SetTitleOffset(1.4);
        frame3.Draw();

        outdir = f'plots_{decay}'
        if not os.path.exists(outdir):
           os.makedirs(outdir)

        print("Saving image!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"as {outdir}/mc_study.png")
        ROOT.gPad.Update()
        c1.SaveAs(f'{outdir}/mc_study_{tag}.png')

        ############################################################################
        # Save the workspace
        # This needs to be first, before its subcomponent PDF's
        getattr(wout,'import')(model)

        for i in range(ntrials):
            result = mcstudy.fitResult(i)
            result.SetName(f'result_{i:05}')
            getattr(wout,'import')(result)
            #wout.Import(result)

        #mcstudy.SetName('mcstudy')
        getattr(wout,'import')(mcstudy)


        n1 = ROOT.TNamed("workspace_filename1",workspace_filename1)
        n2 = ROOT.TNamed("workspace_filename2",workspace_filename2)

        print("Print the contents of the workspace -------------------------")
        wout.Print()

        workspace_outfile.cd()
        n1.Write()
        n2.Write()
        wout.Write()
        workspace_outfile.Close()

        print(f"# successful fits: {nsuccessful_fits} out of {ntrials}")

    ############################################################################


    ########################;
    if len(argv)<=2 or argv[6].find('batch')<0:
        rep = ''
        while not rep in [ 'q', 'Q' ]:
            rep = input( 'enter "q" to quit: ' )
            if 1 < len(rep):
                rep = rep[0]

    return result, mcstudy

################################################################################
if __name__ == '__main__':
    r,m = main(sys.argv)






