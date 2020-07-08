import numpy as np
import matplotlib.pyplot as plt

import sklearn as sk
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, accuracy_score

import sys
import pickle

from sklearn_plot_results import plot_results
import sklearn_tools as sktools

import pandas as pd

# Getting some of this from here
# https://betatim.github.io/posts/sklearn-for-TMVA-users/

################################################################################
infilenames = sys.argv[1:]

outfilename = "CLASSIFICATION_{0}_{1}.pkl".format(infilenames[0].split('.')[0],infilenames[1].split('.')[0])
#outfilename = "test_sklearn.pkl"
outfile = open(outfilename,'wb')

df0,df1 = sktools.read_in_files_and_return_dataframe(infilenames)

print(len(df0),infilenames[0])
print(len(df1),infilenames[1])

#toberemoved = ['bcandmass', 'bcandMES', 'bcandDeltaE', 'pmom', 'lepmom']
# BaBar PID
#toberemoved = ['cos(theta)', 'p3']
toberemoved = []

# Manually remove some of the columns that are about PID
for name in list(df0.keys()):
    if name.find('Is')>=0 or name.find('BDT')>=0 or name.find('KM')>=0:
        toberemoved.append(name)
toberemoved.append('ne')
toberemoved.append('np')
toberemoved.append('nmu')
toberemoved.append('nbnvbcand')
toberemoved.append('bnvbcandMES')
toberemoved.append('bnvbcandDeltaE')
toberemoved.append('bnvbcandmass')
toberemoved.append('bnvlepp3')
toberemoved.append('bnvprotp3')
toberemoved.append('bnvprotp3')
toberemoved.append('pp')
#toberemoved.append('ep')
toberemoved.append('mup')

df0 = sktools.format(df0,'signal',columns_to_drop=toberemoved)
df1 = sktools.format(df1,'background',columns_to_drop=toberemoved)

data = {'df':sktools.mergeDataframes([df0, df1]),
        'zeroClass':'signal', 'oneClass':'background', 'twoClass':'both', 'title':'training data'}

sktools.plot_corr_matrix(data['df'])
#plt.show()

result = sktools.learn(data, hidden_layers=5, iterations=1000)

sktools.tablesReportFromDict(result)
sktools.graphicReport(result)

plt.show()
#exit()


'''
#param_labels = list(dict0.keys())


# For charged modes
#tokeep = ['bnvbcandMES', 'bnvbcandDeltaE', 'tagbcandMES', 'tagbcandDeltaE', 'missingmass', 'missingmom', 'missingE', 'scalarmomsum', 'r2', 'r2all', 'thrustmag', 'thrustmagall', 'thrustcosth', 'thrustcosthall', 'sphericityall', 'ncharged', 'nphot']
# For missing particle modes
#tokeep = ['tagbcandMES', 'tagbcandDeltaE', 'missingmass', 'missingmom', 'missingE', 'scalarmomsum', 'r2', 'r2all', 'thrustmag', 'thrustmagall', 'thrustcosth', 'thrustcosthall', 'sphericityall', 'ncharged', 'nphot']


#for a in toberemoved:
    #if a in param_labels:
        #param_labels.remove(a)

# DO THIS WHEN WE WANT TO REMOVE/KEEP STUFF
#param_labels = tokeep

print(param_labels)
param_labels.remove('cos(theta)')
param_labels.remove('p3')
print(param_labels)

nparams = len(param_labels)
print("nparams: ",nparams)

cuts_to_use = 1

data0 = []
for pl in param_labels:
    #data0.append(dict0[pl]['values'][cuts_to_use])
    #print(pl,len(dict0[pl]['values'][cuts_to_use]))
    # FOR BABAR PID CUTS
    data0.append(list(dict0[pl].values()))
    print(pl,len(dict0[pl]))

data1 = []
for pl in param_labels:
    #data1.append(dict1[pl]['values'][cuts_to_use])
    #print(pl,len(dict1[pl]['values'][cuts_to_use]))
    # FOR BABAR PID CUTS
    data1.append(list(dict1[pl].values()))
    print(pl,len(dict1[pl]))
#exit()

#print(data0[0][0])
#print(type(data0[0][0]))

classifier_results = {}

data0 = np.array(data0)
data1 = np.array(data1)

classifier_results["data0"] = data0
classifier_results["data1"] = data1
classifier_results["param_labels"] = param_labels
classifier_results["dataset0"] = infilenames[0]
classifier_results["dataset1"] = infilenames[1]

################################################################################
# Train test split
################################################################################

X = np.concatenate((data0.transpose(), data1.transpose()))
y = np.concatenate((np.ones(data0.transpose().shape[0]), np.zeros(data1.transpose().shape[0])))
print("X -----------------")
print(type(X),X.shape)
print(type(y),y.shape)
#print(X)
#print(y)

skdataset = {"data":X,"target":y,"target_names":param_labels}

#X_dev,X_eval, y_dev,y_eval = train_test_split(X, y, test_size=0.20, random_state=42)
#X_train,X_test, y_train,y_test = train_test_split(X_dev, y_dev, test_size=0.20, random_state=492)
X_train,X_test, y_train,y_test = train_test_split(X, y, test_size=0.20, random_state=492)

################################################################################
# Fit/Classify
################################################################################

#dt = DecisionTreeClassifier(max_depth=3, min_samples_leaf=0.05*len(X_train))
dt = DecisionTreeClassifier(max_depth=3)

#bdt = AdaBoostClassifier(dt, algorithm='SAMME', n_estimators=800, learning_rate=0.5)
#bdt =  MLPClassifier(alpha=1, max_iter=1000)
bdt =  MLPClassifier(hidden_layer_sizes=(5), max_iter=1000)

print(X_train.shape)
print(y_train.shape)
#print(X_train)
#bdt.fit(X_train, y_train)
bdt.fit(X_train, y_train)

classifier_results["classifier"] = bdt

pickle.dump(classifier_results,outfile)
outfile.close()

plot_results(data0, data1, infilenames[0], infilenames[1], param_labels, bdt)

plt.show()
'''
