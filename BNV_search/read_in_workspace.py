import ROOT
import numpy as np

import sys

def main(argv):

    # Set up a workspace to store everything
    #workspace_filename = "testworkspace.root"
    workspace_filename = argv[1]
    workspace_file = ROOT.TFile(workspace_filename)

    workspace_file.Print()
    workspace_file.ls()

    w = workspace_file.Get("workspace_test")

    w.Print()
    #print(w)

    x = w.var("x");
    x.setBins(1000)
    model = w.pdf("model");

    data = model.generate(ROOT.RooArgSet(x),1000)
    model.fitTo(data)

    xframe = x.frame(ROOT.RooFit.Title("extended ML fit example"))

    data.plotOn(xframe)
    model.plotOn(xframe, ROOT.RooFit.Normalization( 1.0, ROOT.RooAbsReal.RelativeExpected))

    c1 = ROOT.TCanvas("fit1", "fit1", 900, 500)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    xframe.SetAxisRange(0.95,1.0,"X")
    xframe.Draw()
    ROOT.gPad.Update()


    ########################
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]


################################################################################
if __name__ == '__main__':
    main(sys.argv)




