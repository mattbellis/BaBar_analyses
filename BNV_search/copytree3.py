# From here
# https://root.cern.ch/root/html/tutorials/tree/copytree3.C.htm
import gc
import ROOT

import sys

infile = sys.argv[1]
outfile = "testout.root"

# Get old file, old tree and set top branch address
oldfile = ROOT.TFile.Open(infile)
oldtree = oldfile.Get("ntp1");
nentries = oldtree.GetEntries();
#Event *event   = 0;
#oldtree.SetBranchAddress("event",&event);

# Create a new file + a clone of old tree in new file
newfile = ROOT.TFile(outfile,"recreate");
newtree = oldtree.CloneTree(0);

for i in range(nentries):
    if i%10000==0:
        print(i)

    oldtree.GetEntry(i);
    copyflag_prot = False
    copyflag_e = False
    copyflag_mu = False

    for j in range(oldtree.np):
        if oldtree.pp3[j] > 2.0:
            copyflag_prot = True

    for j in range(oldtree.ne):
        if oldtree.ep3[j] > 2.0:
            copyflag_e = True

    for j in range(oldtree.nmu):
        if oldtree.mup3[j] > 2.0:
            copyflag_mu = True


    if copyflag_prot and (copyflag_e or copyflag_mu):
        newtree.Fill();
    
newtree.Print();
newtree.Write();
#newtree.AutoSave();
oldfile.Close()
newfile.Close()

#delete oldfile;
#delete newfile;

gc.collect()
