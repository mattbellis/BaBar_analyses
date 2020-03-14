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

# Getting some of this from here
# https://betatim.github.io/posts/sklearn-for-TMVA-users/

################################################################################
infilenames = sys.argv[1:]
if len(infilenames) != 2:
    print("Wrong number of input files!")
    print("Should be 2!")
    exit()

#outfilename = "CLASSIFICATION_{0}_{1}.pkl".format(infilenames[0].split('.pkl')[0],infilenames[1].split('.pkl')[0])
outfilename = "test_sklearn.pkl"
outfile = open(outfilename,'wb')

dict0 = pickle.load(open(infilenames[0],'rb'))
dict1 = pickle.load(open(infilenames[1],'rb'))

param_labels = list(dict0.keys())

toberemoved = ['bcandmass', 'bcandMES', 'bcandDeltaE', 'pmom', 'lepmom']
# For charged modes
tokeep = ['bnvbcandMES', 'bnvbcandDeltaE', 'tagbcandMES', 'tagbcandDeltaE', 'missingmass', 'missingmom', 'missingE', 'scalarmomsum', 'r2', 'r2all', 'thrustmag', 'thrustmagall', 'thrustcosth', 'thrustcosthall', 'sphericityall', 'ncharged', 'nphot']
# For missing particle modes
tokeep = ['tagbcandMES', 'tagbcandDeltaE', 'missingmass', 'missingmom', 'missingE', 'scalarmomsum', 'r2', 'r2all', 'thrustmag', 'thrustmagall', 'thrustcosth', 'thrustcosthall', 'sphericityall', 'ncharged', 'nphot']


#for a in toberemoved:
    #if a in param_labels:
        #param_labels.remove(a)

param_labels = tokeep

print(param_labels)
nparams = len(param_labels)
print("nparams: ",nparams)

cuts_to_use = 1

data0 = []
for pl in param_labels:
    data0.append(dict0[pl]['values'][cuts_to_use])
    print(pl,len(dict0[pl]['values'][cuts_to_use]))

data1 = []
for pl in param_labels:
    data1.append(dict1[pl]['values'][cuts_to_use])
    print(pl,len(dict1[pl]['values'][cuts_to_use]))
#exit()

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

X_dev,X_eval, y_dev,y_eval = train_test_split(X, y, test_size=0.33, random_state=42)
X_train,X_test, y_train,y_test = train_test_split(X_dev, y_dev, test_size=0.33, random_state=492)

################################################################################
# Fit/Classify
################################################################################

#dt = DecisionTreeClassifier(max_depth=3, min_samples_leaf=0.05*len(X_train))
dt = DecisionTreeClassifier(max_depth=3)

#bdt = AdaBoostClassifier(dt, algorithm='SAMME', n_estimators=800, learning_rate=0.5)
bdt =  MLPClassifier(alpha=1, max_iter=1000)

print(X_train.shape)
print(y_train.shape)
bdt.fit(X_train, y_train)

classifier_results["classifier"] = bdt

pickle.dump(classifier_results,outfile)
outfile.close()

plot_results(data0, data1, infilenames[0], infilenames[1], param_labels, bdt)

plt.show()
