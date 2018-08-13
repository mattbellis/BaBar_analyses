import sys
import ROOT
from array import array
import gc

infilenames = sys.argv[1:]

infile = None
outfile = None
originalTree = None
nevTree = None
selectedTree = None

for infilename in infilenames:

    topdir = infilename.split("out_file")[0]
    basename = infilename.split("/")[-1]
    print("Opening ",basename)
    infile = ROOT.TFile.Open(infilename)

    originalTree = infile.Get("ntp1")
    nev = array( 'i', [ 0 ] )

    # Make tree with one branch
    nevTree = ROOT.TTree("nevTree","A tree with one branch, the number of original events.")
    nevTree.Branch("nev_original",nev,"nev_original/I")
    nev[0] = originalTree.GetEntries()
    nevTree.Fill()

    print("nev: %d" % (nev[0]))

    ROOT.gROOT.cd();
    selectedTree = originalTree.CopyTree("np>0 && ( ne>0 || nmu>0 )")

    # Drop branches
    for branchname in ["gammanCrys", "gammaCentz", "gammaCenty", "gammaCentx"]:
        print(branchname)
        b = selectedTree.GetBranch(branchname)
        selectedTree.GetListOfBranches().Remove(b)


    print("Selected {0} events.".format(selectedTree.GetEntries()))

    #outfilename = "%s/TRIGGER_APPLIED_%s" % (topdir,basename)
    outfilename = "SLIMMED_FILE_%s" % (basename)
    outfile = ROOT.TFile(outfilename,"RECREATE")
    outfile.cd()

    selectedTree.Write()
    nevTree.Write()

    outfile.Close()
    infile.Close()

    gc.collect()
