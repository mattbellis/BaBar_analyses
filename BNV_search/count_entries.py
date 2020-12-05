import sys
import ROOT
import os 

rootdir = sys.argv[1]
infilenames = os.listdir(rootdir)

total = 0
icount = 0
nfiles = len(infilenames)
for infilename in infilenames:

    #print(infilename)

    if infilename.find('.root')<0:
        continue

    filename = "{0}/{1}".format(rootdir,infilename)

    f = ROOT.TFile(filename)
    #f.ls()

    treename = "ntp1"
    if infilename.find('SKIMMED_PID')>=0:
        treename = 'Tskim'

    if f.GetNkeys()>0:

        t = f.Get(treename)

        total += t.GetEntries()
        print(icount,nfiles,"\t\t",infilename,total)
    icount += 1

print("Total: {0}   {1}".format(total,infilenames[0].split('-R24')[0]))



