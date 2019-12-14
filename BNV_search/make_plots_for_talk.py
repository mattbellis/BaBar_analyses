import sys

import ROOT
import matplotlib.pylab as plt

f = ROOT.TFile(sys.argv[1])
#f.ls()

#t = f.Get("Tskim")
t = f.Get("analysis")
#t.Print()

nentries = t.GetEntries()

tagmes = []
tagdE = []
tagbcand = []

missingmass = []
missingmom = []
missingE = []

for i in range(nentries):

    t.GetEntry(i)

    if t.nproton==1 and t.protone[0]>2.3 and t.nhighmom==1 and t.nmu==0 and t.ne==0:# and t.tagq==0:
    #if 1:
    #if t.nproton==0 and t.nmu==1 and t.mue[0]>2.0:
        tagmes.append(t.tagmes)
        tagdE.append(t.tagdE)
        tagbcand.append(t.tagbcand)

        missingmass.append(t.missingmass)
        missingmom.append(t.missingmom)
        missingE.append(t.missingE)



print(len(tagbcand))

plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.hist(tagbcand,bins=100,range=(0,13))
plt.xlabel(r'tag-B mass [GeV/c$^2$]',fontsize=14)

plt.subplot(1,3,2)
plt.hist(tagmes,bins=100,range=(5.0,5.3))
plt.xlabel(r'tag-B M$_{ES}$ [GeV/c$^2$]',fontsize=14)

plt.subplot(1,3,3)
plt.hist(tagdE,bins=100,range=(-5.0,10.))
plt.xlabel(r'tag-B $\Delta$E [GeV]',fontsize=14)

plt.tight_layout()

idx = sys.argv[1].find('SP')
plt.savefig(sys.argv[1][idx:idx+8]+'_EXPLORATORY_CUTS_0.png')


plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.hist(missingmass,bins=100,range=(-20,20))
plt.xlabel(r'Missing mass [GeV/c$^2$]',fontsize=14)

plt.subplot(1,3,2)
plt.hist(missingmom,bins=100,range=(0,6))
plt.xlabel(r'Missing p [GeV/c]',fontsize=14)

plt.subplot(1,3,3)
plt.hist(missingE,bins=100,range=(-5,10))
plt.xlabel(r'Missing E [GeV]',fontsize=14)

plt.tight_layout()

plt.savefig(sys.argv[1][idx:idx+8]+'_EXPLORATORY_CUTS_1.png')

#c1 = ROOT.TCanvas("c1","c1",900,300)
#c1.Divide(1,3)
#c1.cd(1)
#h1 = ROOT.TH1F("h1","h1",100,5.0,5.3)
#t.Draw("tagmes>>h1","tagmes>5.0")
#h1.GetXaxis("tag-B M_{ES} "
#
plt.show()
