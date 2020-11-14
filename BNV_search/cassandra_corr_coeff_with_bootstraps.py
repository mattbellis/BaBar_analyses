import matplotlib.pylab as plt
import numpy as np
import sys
import pandas as pd
import seaborn as sns

infilename = sys.argv[1]

#var_to_test = 'bnvbcandMES'
var_to_test = 'bnvbcandDeltaE'


df = pd.read_hdf(infilename)


columns =    [#'nbnvbcand', \
        #'bnvbcandmass', \
                'bnvbcandMES', \
                'bnvbcandDeltaE', \
                #'bnvprotp3', \
                #'bnvlepp3', \
                'tagbcandmass', \
                'tagbcandMES', \
                'tagbcandDeltaE', \
                'tagq', \
                'missingmass', \
                'missingmom', \
                'missingE', \
                'scalarmomsum', \
                #'nhighmom', \
                #'np', \
                #'nmu', \
                #'ne', \
                #'pp', \
                #'mup', \
                #'ep', \
                'r2',  \
                'r2all', \
                'thrustmag', \
                'thrustmagall', \
                'thrustcosth', \
                'thrustcosthall', \
                'sphericityall', \
                'ncharged', \
                'nphot']

columns = np.array(columns)

col = df[columns]

def correlation(col, var, max_vars=None):
    means_MES = []    
    uncertainty_MES = []
    not_corr_MES = []
    not_corr_corr_MES = []
    
    ccs = []
    cc_uncerts = []
    cc_measureds = []
    vars_tested = []
    
    nvars_measured = 0
    
    print("Variables correlated with ", var)
    for ii in col:
        y = df[var].values
        x = df[ii].values
    
        datacov = np.array([x,y]).T
        nsamples = 100
        sample_corrcoefs = []
        indices = np.arange(0,len(datacov),1).astype(int)

        x,y = datacov.transpose()

        cc_meas = np.corrcoef(x,y)[0][1]
        for n in range(nsamples):
            sample_indices = np.random.choice(indices,len(indices),replace=True)
            sample_data = datacov[sample_indices]
            x,y = sample_data.transpose()
            sample_corrcoefs.append(np.corrcoef(x,y)[0][1])   


        ccs.append(np.mean(sample_corrcoefs))
        cc_uncerts.append(np.std(sample_corrcoefs))
        cc_measureds.append(cc_meas)
        vars_tested.append(ii)
        
        print("%-23s Bootstrapping mean: %1.5f, +/-: %1.5f, \t corr coeff: %1.5f" %(\
            ii, np.mean(sample_corrcoefs), np.std(sample_corrcoefs), cc_meas))
        
        nvars_measured += 1
        
        if max_vars is not None:
            if nvars_measured>=max_vars:
                break

    return ccs,cc_uncerts,cc_measureds,vars_tested
        


max_vars = None

ccs,cc_uncerts,cc_measureds,vars_tested = correlation(col[columns[columns!=var_to_test]], var_to_test ,max_vars=max_vars)



plt.figure(figsize=(15,6))

plt.errorbar(vars_tested, ccs, cc_uncerts,fmt='o')  #label=columns[0:max_vars])
plt.plot([-1,len(columns)],[0,0],'k--')
plt.xlabel('variable')
plt.ylabel('Correlation coefficient')
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("ccs_with_uncertainties_{0}_{1}.png".format(infilename.split('.h5')[0],var_to_test))

plt.show()

