import sys
import numpy as np
import pickle

infilenames = sys.argv[1:3]


if len(infilenames)!=2:
    print("Wrong number of infiles!")
    exit()

print(infilenames)
outfilename = "{0}_{1}.pkl".format(infilenames[0].split('.pkl')[0], infilenames[1].split('.pkl')[0])

infiles = []
for name in infilenames:
    infiles.append(pickle.load(open(name,'rb')))

print(infiles[0].keys())
print(infiles[1].keys())

outdict = {}
for varkey in infiles[0].keys():
    outdict[varkey] = {}
    print("----------")
    print(varkey)
    for key in infiles[0][varkey].keys():
        print(key)
        if key != "values":
            outdict[varkey][key] = infiles[0][varkey][key]
        else:
            vals0 = infiles[0][varkey][key]
            vals1 = infiles[1][varkey][key]
            print(type(vals0),len(vals0))
            totvals = []
            for v0,v1 in zip(vals0,vals1):
                print(len(v0),len(v1),type(v0[0]))
                totvals.append(np.concatenate([v0,v1]))
            print(len(totvals),len(totvals[0]),len(totvals[1]))
            outdict[varkey][key] = totvals

outfile = open(outfilename,'wb')
pickle.dump(outdict,outfile)
outfile.close()
