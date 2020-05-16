import sys
import ROOT

infilenames = sys.argv[1:]

total = 0
for infilename in infilenames:

    f = ROOT.TFile(infilename)

    if f.GetNkeys()>0:

        t = f.Get("ntp1")

        total += t.GetEntries()
        print(infilename,total)

print("Total: {0}".format(total))



