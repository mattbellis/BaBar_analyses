import sys
import ROOT
import os 

rootdir = sys.argv[1]
infilenames = os.listdir(rootdir)

total = 0
for infilename in infilenames:

    if infilename.find('.root')<0:
        continue

    filename = "{0}/{1}".format(rootdir,infilename)

    f = ROOT.TFile(filename)

    if f.GetNkeys()>0:

        t = f.Get("ntp1")

        total += t.GetEntries()
        print(infilename,total)

print("Total: {0}   {1}".format(total,infilenames[0].split('-R24')[0]))



