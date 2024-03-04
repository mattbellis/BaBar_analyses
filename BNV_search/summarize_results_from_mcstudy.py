import ROOT
import numpy as np

import sys

import matplotlib.pylab as plt

infilenames = sys.argv[1:]

means = []
nsigs = []
sigmas = []

import seaborn as sns
import pandas as pd

decay = None
decays = ['pnu','pe','pmu','ne','nmu']
for d in decays:
    if infilenames[0].find(f'_{d}_')>=0:
        decay = d
        break

sptrain = None
sptrains = ['SP998', 'SP1005']
for s in sptrains:
    if infilenames[0].find(f'_{s}')>=0:
        sptrain = s
        break




all_nsigs = []
all_nsigs_for_scatter = []
all_fitsigs = []

all_errs = []

ntests = 0

n_significant = []
pct_significant = []

for infilename in infilenames:

    print(f"Opening {infilename}")
    infile = ROOT.TFile(infilename)

    w = infile.Get('workspace_trials')
    #mcstudy = infile.Get('mcstudy')
    #print(mcstudy)

    ntrials = int(infilename.split('ntrials_')[-1].split('_')[0])
    nsiginit = int(infilename.split('nsig_')[-1].split('_')[0])

    ntests += 1

    vals = []
    errs = []
    x = []
    nsignificant = 0
    for i in range(ntrials):
        name = f'result_{i:05}'
        try:
            r = w.genobj(name)
        except:
            print("ROOT file is not closed probably...can't extract RooWorkspace object")
            continue

        # Pulls?
        # https://root-forum.cern.ch/t/roomcstudy-pull-calculation-and-getting-generated-values-of-parameters/37359
        nsig = r.floatParsFinal().find('nsig')

        v = nsig.getVal()
        e = nsig.getError()

        x.append(i)
        errs.append(e)
        vals.append(v)

        # Check to see if it is a significant fit
        if v-(2*e)>0:
            nsignificant += 1

        #print(v)

    #plt.figure()
    #plt.errorbar(x,vals,yerr=errs,fmt='o')

    #plt.figure()
    #plt.hist(vals,bins=40)

    means.append(np.mean(vals))
    sigmas.append(np.std(vals))
    nsigs.append(nsiginit)
    n_significant.append(nsignificant)
    pct_significant.append(nsignificant/ntrials)

    all_fitsigs += vals
    all_errs += errs
    all_nsigs += len(vals)*[nsiginit]
    all_nsigs_for_scatter += np.linspace(nsiginit-25, nsiginit+25,len(vals)).tolist()
    #print(all_nsigs)

#print(vals)
#print(errs)

#plt.

print(nsigs)
print(means)

################################################################################
plt.figure()
plt.errorbar(nsigs, means, yerr=sigmas,fmt='o',markersize=5)
lo = min(nsigs)
hi = max(nsigs)
print(lo,hi)
plt.plot([lo,hi],[lo,hi],'k--')
plt.xlabel('True # of signal events',fontsize=14)
plt.ylabel('Fit # of signal events',fontsize=14)
#plt.xlim(-500,12000)
#plt.ylim(-100,12000)
#plt.xlim(-50,1200) # pnu
#plt.ylim(-10,1200)
plt.xlim(-500,12000)
plt.ylim(-500,12000)
plt.tight_layout()

plt.savefig(f"plots_{decay}/mcstudy_summaries_{decay}_{sptrain}_00.png")

print(f"ntests: {ntests}")
width = (hi-lo)
if ntests > 1:
    width = (hi-lo)/(ntests-1)

# This never really worked that well
#df = pd.DataFrame({"nsig":all_nsigs, "fitvals":all_fitsigs})
#plt.figure()
#sns.violinplot(x=df['nsig'], y=df['fitvals'])
#lox,hix = plt.gca().get_xlim()
#loy,hiy = plt.gca().get_ylim()
#print(lox,hix)
#print(loy,hiy)
#Xlo = lo/width + lox - 0.5
#Xhi = hi/width + lox - 0.5
#print(Xlo,Xhi, width)
#plt.plot([Xlo,Xhi],[lo,hi],'k--')

plt.figure()
x = np.arange(0,len(all_errs))
plt.errorbar(all_nsigs_for_scatter,all_fitsigs,yerr=all_errs,fmt='k.',ecolor='blue')
plt.plot([min(all_nsigs_for_scatter),max(all_nsigs_for_scatter)],[0,0],'k--')
plt.xlabel('True # of signal events',fontsize=14)
plt.ylabel('Fit # of signal events',fontsize=14)
plt.plot([lo,hi],[lo,hi],'k--')
#plt.xlim(-500,12000)
#plt.ylim(-12000,12000)
#plt.xlim(-50,1200)   # pnu
plt.xlim(-500,10000)
plt.tight_layout()
plt.savefig(f"plots_{decay}/mcstudy_summaries_{decay}_{sptrain}_01.png")


plt.figure()
plt.plot(nsigs,pct_significant,'o', markersize=10)
plt.xlabel('True # of signal events',fontsize=14)
plt.ylabel('% of toy studies with significant signal',fontsize=14)
#plt.xlim(-500,12000) 
#plt.ylim(0)
#plt.xlim(-50,1200) # pnu
#plt.ylim(0)
plt.xlim(-500,10000)
plt.tight_layout()
plt.savefig(f"plots_{decay}/mcstudy_summaries_{decay}_{sptrain}_02.png")



plt.show()


