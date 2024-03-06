import sys

import tensorflow as tf # not set up for gpu yet (I don't think)
import numpy as np
import pandas as pd

import sklearn_tools as sktools

import plotting_tools as pt

from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model

from matplotlib import pyplot

#tag = 'pmu_1005'

# **********************************************
# Output: dataset without specified 
#           rows/columns, additional "Class" 
#           column
# **********************************************
def format(df, columnsToDrop, rowsToDrop, className=None):
  # The errors='ignore' means that if the column is not there, no error is thrown
  df = df.drop(columns=columnsToDrop, errors='ignore') # remove specified columns
  #print(rowsToDrop)
  #df = df.drop(rowsToDrop) # remove specified rows

  if className != None:
    # add column with class name
    labels = [className] * len(df) #list of labels is the length of the df
    df['Class'] = labels # creates new class column

  return df # returns data frame with new class and reformatted


# **********************************************
# Input: list of datsets to be merged
# Output: one merged dataframe
# **********************************************
def mergeDataframes(dfs):
  mergedDfs = pd.DataFrame()

  for df in dfs:
    mergedDfs = pd.concat([mergedDfs, df])
    
  return mergedDfs
################################################################################


infilenames = sys.argv[1:]


df0,df1 = sktools.read_in_files_and_return_dataframe(infilenames)

print(df0.columns)
print()
print(df1.columns)
cols = df1.columns

print("Size of files!")
print(len(df0),infilenames[0])
print(len(df1),infilenames[1])

print(df0.columns)
print()
print(df1.columns)
print()

#exit()

toberemoved = []

#'''
# Manually remove some of the columns that are about PID
# BaBar
#'''
for name in list(df0.keys()):
    if name.find('Is')>=0 or name.find('BDT')>=0 or name.find('KM')>=0:
        toberemoved.append(name)
#'''

################################################################################
# For SP-11975, pnu
################################################################################
#'''
# MAYBE???
toberemoved.append('ne')
toberemoved.append('np')
toberemoved.append('nmu')
#toberemoved.append('bnvbcandMES')
#toberemoved.append('bnvbcandDeltaE')
toberemoved.append('bnvbcandmass')
toberemoved.append('nbnvbcand')
#toberemoved.append('tagbcandmass')
toberemoved.append('nhighmom')
toberemoved.append('bnvlepp3')
toberemoved.append('bnvprotp3')
toberemoved.append('pp')
toberemoved.append('ep')
toberemoved.append('mup')
#'''

################################################################################
# For SP-11976, nmu
# For SP-11977, ne
################################################################################
'''
#toberemoved.append('ne')
#toberemoved.append('np')
#toberemoved.append('nmu')
#toberemoved.append('bnvbcandMES')
#toberemoved.append('bnvbcandDeltaE')
#toberemoved.append('missingmass') # NEED TO CHECK
#toberemoved.append('missingmassES') # NEED TO CHECK
#toberemoved.append('missingmass2') # NEED TO CHECK
#toberemoved.append('bnvbcandp3') # NEED TO CHECK
#toberemoved.append('bnvprotcosth') # NEED TO CHECK
#toberemoved.append('bnvlepcosth') # NEED TO CHECK
#toberemoved.append('tagbcandp3') # NEED TO CHECK
toberemoved.append('bnvbcandmass')
toberemoved.append('nbnvbcand')
#toberemoved.append('tagbcandmass')
toberemoved.append('nhighmom')
toberemoved.append('bnvlepp3')
#toberemoved.append('bnvprotp3')
toberemoved.append('pp')
toberemoved.append('ep')
toberemoved.append('mup')
'''

for tbr in toberemoved:
    if tbr in cols:
        print("Yes! ",tbr)
    else:
        print("No! ",tbr)



#df0 = format(df0, ['cos(theta)', 'p3'], 0, 'positive')
#df1 = format(df1, ['cos(theta)', 'p3'], 0, 'negative')
df0 = format(df0, toberemoved, 0, 'positive')
df1 = format(df1, toberemoved, 0, 'negative')
#df = mergeDataframes([df0[0:100000], df1[0:100000]])
#df = mergeDataframes([df0[0:50000], df1[0:50000]])
#df = mergeDataframes([df0[100000:200000], df1[100000:200000]])
df = mergeDataframes([df0, df1])

# Get rid of nans
df.dropna(0,inplace=True)

print("Merged and dropped columns!")
print(df.columns)
print()
#exit()


# split into input and output columns
y = df.pop('Class') # all class values become 'y'
X = df

print("Lenth of X and y!")
print(len(X))
print(len(y))

# ensure all data are floating point values
X = X.astype('float32')
# encode strings to integer
y = LabelEncoder().fit_transform(y)
# split into train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

#.shape returns the dimensions of the dataset. So (48778, 18) means 48778 rows and 18 columns
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape) 

# determine the number of input features
n_features = X_train.shape[1] # 2nd item returned by ".shape" is the # of columns/features


print(y[0:10])
print(y[40000:40010])

# define model
model = Sequential()
model.add(Dense(10, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
model.add(Dense(8, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(1, activation='sigmoid'))

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# fit the model
history = model.fit(X_train, y_train, epochs=105, batch_size=100, validation_split=0.3, verbose=1)
#history = model.fit(X_train, y_train, epochs=105, batch_size=100, validation_split=0.5, verbose=1)
# evaluate the model
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print('Test Accuracy: %.3f' % acc)

# make a prediction
row = X_test.iloc[[0]] # row/one particle to run prediction on
yhat = model.predict([row]) # makes prediction
print('Predicted: %.3f' % yhat) # 1 = proton, 0 = not proton

model.summary()
#model.save('keras_model')

# EDIT SO PLOTS ARE SAVED IN COMMON LOCATION
#t,l,d = pt.get_sptag(infilenames[0])
#print(d)
#exit()

tag = '{0}_{1}'.format(infilenames[0].split('.h5')[0],infilenames[1].split('.h5')[0])
modelfilename = 'KERAS_TRAINING_{0}.h5'.format(tag)

#model.save('TT_keras_model.h5')
model.save(modelfilename)

sktools.compare_train_test(model, X_train, y_train, X_test, y_test, bins=200,tag=tag)



# summarize the model
plot_model(model, 'model.png', show_shapes=True)


# plot learning curves
pyplot.figure()
pyplot.title('Learning Curves')
pyplot.xlabel('Epoch')
pyplot.ylabel('Cross Entropy')
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='val')
pyplot.legend()
pyplot.savefig('keras_learning_curve' + tag + '.png')

from sklearn.metrics import roc_curve
y_pred_keras = model.predict(X_test).ravel()
fpr_keras, tpr_keras, thresholds_keras = roc_curve(y_test, y_pred_keras)

from sklearn.metrics import auc
auc_keras = auc(fpr_keras, tpr_keras)

from sklearn.ensemble import RandomForestClassifier
# Supervised transformation based on random forests
rf = RandomForestClassifier(max_depth=3, n_estimators=10)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict_proba(X_test)[:, 1]
fpr_rf, tpr_rf, thresholds_rf = roc_curve(y_test, y_pred_rf)
auc_rf = auc(fpr_rf, tpr_rf)

from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=5, max_iter=1000, verbose=True)
# fit function: trains algorithm on training data
mlp_model = mlp.fit(X_train, y_train)
y_pred_mlp = mlp.predict_proba(X_test)[:, 1]
fpr_mlp, tpr_mlp, thresholds_mlp = roc_curve(y_test, y_pred_mlp)
auc_mlp = auc(fpr_mlp, tpr_mlp)

data_to_save = {}
data_to_save['fpr_keras'] = fpr_keras
data_to_save['tpr_keras'] = tpr_keras
data_to_save['thresholds_keras'] = thresholds_keras
df_out = pd.DataFrame.from_dict(data_to_save)
df_out.to_hdf('roc_out_{0}.h5'.format(tag),'df_out')

pyplot.figure()
pyplot.plot([0, 1], [0, 1], 'k--')
pyplot.plot(fpr_keras, tpr_keras, label='Keras (area = {:.3f})'.format(auc_keras))
pyplot.plot(fpr_rf, tpr_rf, label='RF (area = {:.3f})'.format(auc_rf))
pyplot.plot(fpr_mlp, tpr_mlp, label='MLP (area = {:.3f})'.format(auc_mlp))
pyplot.xlabel('False positive rate')
pyplot.ylabel('True positive rate')
pyplot.title('ROC curve')
pyplot.legend(loc='best')
pyplot.savefig('keras_roc_curve' + tag + '.png')
#pyplot.show()
'''
# Zoom in view of the upper left corner.
pyplot.figure()
pyplot.xlim(0, 0.2)
pyplot.ylim(0.8, 1)
pyplot.plot([0, 1], [0, 1], 'k--')
pyplot.plot(fpr_keras, tpr_keras, label='Keras (area = {:.3f})'.format(auc_keras))
pyplot.plot(fpr_rf, tpr_rf, label='RF (area = {:.3f})'.format(auc_rf))
pyplot.xlabel('False positive rate')
pyplot.ylabel('True positive rate')
pyplot.title('ROC curve (zoomed in at top left)')
pyplot.legend(loc='best')
'''


pyplot.show()

# this curve shows underfitting. How to fix?


