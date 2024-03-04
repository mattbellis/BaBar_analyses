import ROOT
import numpy as np

import sys
import os

from pdf_definitions import read_in_ML_output
from pdf_definitions import argus_in_x,read_in_ML_output,two_argus_in_x,three_argus_in_x
from pdf_definitions import argus_in_x,read_in_ML_output,two_argus_in_x,three_argus_in_x,two_argus_plus_expon_in_x

import plotting_tools as pt

def main(argv):

    constraint_multiplier = 0.6
    nentries = 30000
    nsiginit = 1000
    ntrials = 20

    # Set up a workspace to store everything
    #workspace_filename = "testworkspace.root"
    print("Read in signal.............")
    workspace_filename = argv[1]
    workspace_filename_tag_SIG = pt.get_tags(workspace_filename,ftype='workspace')
    print(workspace_filename_tag_SIG)
    #exit()

    tag,label,decay = pt.get_sptag(workspace_filename)
    print(tag,label,decay)
    # Decay probably is something like _ne_ so remove the underscores
    decay = decay[1:-1]
    print(tag,label,decay)
    outdir = f'plots_{decay}'

    workspace_file = ROOT.TFile(workspace_filename)
    workspace_file.Print()
    workspace_file.ls()
    w = workspace_file.Get("workspace")
    w.Print()
    variable_dict = {}
    variables_to_constrain = []
    #print(w)
    for v in w.allVars():
        print(v)
        name = v.GetName()
        val = v.getVal()
        err = v.getError()
        #variable_dict[name] = [val,err]
        variable_dict[name] = v

        if name != 'x' and name[0]!='n':
            #v.setConstant(ROOT.kTRUE)
            # Or
            v.setRange(val-(constraint_multiplier*err),val+(constraint_multiplier*err))

            variables_to_constrain.append(name)
            
            # Make terms for the gaussian constraints
            newname = f'{name}_nominal'
            variable_dict[newname] = ROOT.RooRealVar(newname,newname,val)
            variable_dict[newname].setConstant(True)

            newname = f'{name}_err'
            variable_dict[newname] = ROOT.RooRealVar(newname,newname,err)
            variable_dict[newname].setConstant(True)


    x = w.var("x");
    x.setRange(0.2,1.0) # Just for nmu for now
    if decay=='pmu':
        x.setRange(5.2,5.3) # Just for nmu for now
    elif decay=='nmu':
        x.setRange(0.2,1.0) # Just for nmu for now

    x.setBins(50)

    # Get the signal model
    model_sig = w.pdf("model_sig");
    nsig = w.var("nsig");

    # Background
    print("Read in background.............")
    workspace_filename = argv[2]
    workspace_filename_tag_BKG = pt.get_tags(workspace_filename,ftype='workspace')
    print(workspace_filename_tag_BKG)

    workspace_file = ROOT.TFile(workspace_filename)
    workspace_file.Print()
    workspace_file.ls()
    w = workspace_file.Get("workspace")
    w.Print()
    #print(w)
    print("Background variables...")

    for v in w.allVars():
        print(v)
        name = v.GetName()
        val = v.getVal()
        err = v.getError()
        #variable_dict[name] = [val,err]
        variable_dict[name] = v
        if name != 'x' and name[0]!='n':
            #v.setConstant(ROOT.kTRUE)
            # Or
            v.setRange(val-(constraint_multiplier*err),val+(constraint_multiplier*err))

            variables_to_constrain.append(name)

            # Make terms for the gaussian constraints
            newname = f'{name}_nominal'
            variable_dict[newname] = ROOT.RooRealVar(newname,newname,val)
            variable_dict[newname].setConstant(True)

            newname = f'{name}_err'
            variable_dict[newname] = ROOT.RooRealVar(newname,newname,err)
            variable_dict[newname].setConstant(True)


        # Lock down the shape parameters for the signal
        if name[0]!='n' and name.find('sig'):
            v.setRange(val-(0.001*err),val+(0.001*err))

    print(variable_dict)

    ############################################################################
    infilename = argv[3]
    infilename_tag = pt.get_tags(infilename,ftype='infile')

    savefile_tag = f'{infilename_tag}_SIG_{workspace_filename_tag_SIG}_BKG_{workspace_filename_tag_BKG}'

    x = ROOT.RooRealVar("x", "x", 0.2, 1.0)
    if decay=='pmu':
        x = ROOT.RooRealVar("x", "x", 5.2, 5.3)
    x.setBins(50)
    #x.setBins(200)

    # Read in the data
    #data = read_in_ML_output(infilename,x,max_vals=None)
    data = read_in_ML_output(infilename,x,max_vals=1000000)
    ############################################################################


    #exit()

    # Get the background model
    model_bkg = w.pdf("model_bkg");
    nbkg = w.var("nbkg");

    nsig.setVal(nsiginit)
    nsig.setRange(1,nentries)
    nbkg.setVal(nentries-nsiginit)
    nbkg.setRange(0,nentries)

    model = ROOT.RooAddPdf("model","n1*a1 + n2*a2",ROOT.RooArgList(model_sig, model_bkg), ROOT.RooArgList(nsig, nbkg))
    nll = model.createNLL(data);
    nll.SetName('nll')
    
    ####################################################################################################################
    # From LambdaC analysis
    # cutoff0_bkg
    #'''
    #cutoff0_bkg_nominal = ROOT.RooRealVar("cutoff0_bkg_nominal","cutoff0_bkg_nominal",0.993608)
    #cutoff0_bkg_nominal.setConstant(True)
    #cutoff0_bkg_err = ROOT.RooRealVar("cutoff0_bkg_err","cutoff0_bkg_err",0.0054205)
    #cutoff0_bkg_err.setConstant(True)

    ''' This works
    log_gc = ROOT.RooFormulaVar("log_gc","(cutoff0_bkg_nominal-cutoff0_bkg)*(cutoff0_bkg_nominal-cutoff0_bkg)/(2.0*cutoff0_bkg_err*cutoff0_bkg_err)", \
            #ROOT.RooArgList(variable_dict['cutoff0_bkg_nominal'],variable_dict['cutoff0_bkg'],variable_dict['cutoff0_bkg_nominal'],variable_dict['cutoff0_bkg'],variable_dict['cutoff0_bkg_err'],variable_dict['cutoff0_bkg_err']))
        ROOT.RooArgList(variable_dict['cutoff0_bkg_nominal'],variable_dict['cutoff0_bkg'],variable_dict['cutoff0_bkg_err'])) # Just list the variables once
    '''
    #exit()

    #'''
    gc_funcs = {}
    for name in variables_to_constrain:
        nom_name = f'{name}_nominal'
        err_name = f'{name}_err'
        eqn_name = f"({nom_name} - {name})*({nom_name} - {name})/(2.0*{err_name}*{err_name})"
        print(eqn_name)
        formula_name = f'log_gc_{name}'
        log_gc = ROOT.RooFormulaVar(formula_name,eqn_name,ROOT.RooArgList( \
                variable_dict[nom_name], \
                variable_dict[name], \
                #variable_dict[nom_name], \
                #variable_dict[name], \
                #variable_dict[err_name], \
                variable_dict[err_name] \
                ))
        gc_funcs[formula_name] = log_gc
     #'''

    #results = model.fitTo(data,ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.RooCmdArg(SetMaxCalls))

    # Create the NLL for the fit
    #nll = RooNLLVar("nll","nll",total,reduced_data,RooFit.Extended(kTRUE))
    # This works
    #fit_func = ROOT.RooFormulaVar("fit_func","nll + log_gc",ROOT.RooArgList(nll,log_gc))

    func_string = "nll "
    arglist = ROOT.RooArgList(nll)
    for name in gc_funcs.keys():
        func_string += f" + {name}"
        arglist.add(gc_funcs[name])

    print("hhhhhhhhhhhhhhhhhhh")
    print(func_string)
    print()

    fit_func = ROOT.RooFormulaVar("fit_func",func_string,arglist)

    #m = ROOT.RooMinuit(fit_func)
    m = ROOT.RooMinimizer(fit_func)
    m.setVerbose(ROOT.kFALSE)
    m.migrad()
    #m.hesse()

    print("Got to this point!!!!!")
    exit()
    #'''
    ####################################################################################################################



    m = ROOT.RooMinimizer(nll)

    # Activate verbose logging of MINUIT parameter space stepping
    m.setVerbose(ROOT.kTRUE);
    # Call MIGRAD to minimize the likelihood
    m.migrad();
    results = m.save();

    exit()
    
    ############################################################################
    # Plot things
    ############################################################################
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

    outdir = f'plots_{decay}'
    if not os.path.exists(outdir):
       os.makedirs(outdir)

    ROOT.gPad.Update()
    #c.SaveAs("fit_to_data.png")
    #outfile = f"{outdir}/fit_to_data_{infilename_tag}_SIG_{workspace_filename_tag_SIG}_BKG_{workspace_filename_tag_BKG}.png"
    outfile = f"{outdir}/fit_to_data_{savefile_tag}.png"
    print(outfile)
    c.SaveAs(outfile)
    #exit()

    # Draw the frame on the canvas
    c1 = ROOT.TCanvas("fit1", "fit1", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    #xframe.SetAxisRange(0.98,1.0,"X")
    xframe.SetAxisRange(0.90,1.0,"X")
    xframe.SetAxisRange(0.0,20.0,"Y") # nmu, fit Run 1
    if decay=='pmu':
        xframe.SetAxisRange(5.20,5.3,"X")
    xframe.Draw()
    #xframe.SetMaximum(10000)
    ROOT.gPad.Update()
    #c1.SaveAs("fit_to_data1.png")
    outfile = f"{outdir}/fit_to_data_ZOOM_{savefile_tag}.png"
    print(outfile)
    c1.SaveAs(outfile)
    #c1.SaveAs(f"{outdir}/fit_to_data_ZOOM_{infilename}.png")

    ############################################################################
    # PROFILE LIKELHOOD
    # https://roostatsworkbook.readthedocs.io/en/latest/docs-plr.html
    #
    plCalc = ROOT.RooStats.ProfileLikelihoodCalculator(data,model,ROOT.RooArgList(nsig))
    plCalc.SetConfidenceLevel(0.90)
    interval = plCalc.GetInterval()

    #poi = model.GetParametersOfInterest("sig")
    lowerLimit = interval.LowerLimit(nsig)
    upperLimit = interval.UpperLimit(nsig)
    print(f"RESULT:  {100*plCalc.ConfidenceLevel()}  % interval is : [{lowerLimit} , {upperLimit}]\n")

    cllp = ROOT.TCanvas("cllp", "cllp", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)

    llpplot = ROOT.RooStats.LikelihoodIntervalPlot(interval);
    #plot->SetNPoints(50);   // Use this to reduce sampling granularity (trades speed for precision)
    llpplot.Draw("TF1")
    ROOT.gPad.Draw()
    ROOT.gPad.Update()
    #cllp.SaveAs(f"{outdir}/likelihoodintervalplot_{infilename}.png")
    outfile = f"{outdir}/likelihoodintervalplot_{savefile_tag}.png"
    print(outfile)
    cllp.SaveAs(outfile)
    #cllp.SaveAs(f"{outdir}/likelihoodintervalplot_{infilename_tag}_SIG_{workspace_filename_tag_SIG}_BKG_{workspace_filename_tag_BKG}.png")
    #cllp.SaveAs(f"{outdir}/fit_to_data_ZOOM_{infilename}_SIG_{workspace_filename_SIG}_BKG_{workspace_filename_BKG}.png")

    ############################################################################


    pll_frac = None
    framescan = None

    ''''
    # NLL scan
    c2 = ROOT.TCanvas("scan", "scan", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)

    lo = 0
    hi = nsig.getVal() + 4*nsig.getError()
    print(lo,hi)
    #exit()

    #framescan = nsig.frame(ROOT.RooFit.Bins(10),ROOT.RooFit.Range(1,200),ROOT.RooFit.Title("LL and profileLL in nsig"))
    framescan = nsig.frame(ROOT.RooFit.Bins(10),ROOT.RooFit.Range(lo,hi),ROOT.RooFit.Title("LL and profileLL in nsig"))
    nll.plotOn(framescan,ROOT.RooFit.ShiftToZero()) 

    # The profile likelihood estimator on nll for frac will minimize nll w.r.t
    # all floating parameters except nsig for each evaluation
    pll_frac = nll.createProfile(ROOT.RooArgSet(nsig)) ;
    # Plot the profile likelihood in frac
    pll_frac.plotOn(framescan,ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.ShiftToZero()) ;

    framescan.GetYaxis().SetTitleOffset(1.4)
    #framescan.SetAxisRange(0.0,1.0,"Y")
    #framescan.SetAxisRange(0.0,nsig.getVal() + 3* nsig.getError(),"X")
    framescan.Draw()
    framescan.SetMaximum(100)
    framescan.SetMinimum(0)
    ROOT.gPad.Update()
    c2.SaveAs(f"{outdir}/fit_to_data_NLL_scan_{infilename}.png")
    ROOT.gPad.Update()
    '''
    #'''


    print("Print the results -------------------------")
    results.Print("v")

    print(f"RESULT:  {100*plCalc.ConfidenceLevel()}  % interval is : [{lowerLimit} , {upperLimit}]\n")


    print(argv)
    print(argv[4])
    ########################;
    if len(argv)<=4 or argv[4].find('batch')<0:
        rep = ''
        while not rep in [ 'q', 'Q' ]:
            rep = input( 'enter "q" to quit: ' )
            if 1 < len(rep):
                rep = rep[0]

    return results,framescan,pll_frac,nll

################################################################################
if __name__ == '__main__':
    results, framescan, pll_frac, nll = main(sys.argv)




