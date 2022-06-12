import sys

import tensorflow as tf # not set up for gpu yet (I don't think)
import numpy as np
import pandas as pd

import sklearn_tools as sktools

from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model

from tensorflow import keras

from matplotlib import pyplot

modelfilename = sys.argv[1]

datafilename = sys.argv[2]

model = keras.models.load_model(modelfilename)

df,df = sktools.read_in_files_and_return_dataframe([datafilename,datafilename])

#'''
# Manually remove some of the columns that are about PID
# BaBar
toberemoved = []
for name in list(df.keys()):
    if name.find('Is')>=0 or name.find('BDT')>=0 or name.find('KM')>=0:
        toberemoved.append(name)
'''
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
#toberemoved.append('ep')
#toberemoved.append('mup')
'''
# pnu
'''
toberemoved.append('bnvbcandmass')
toberemoved.append('nbnvbcand')
#toberemoved.append('tagbcandmass')
toberemoved.append('nhighmom')
toberemoved.append('bnvlepp3')
#toberemoved.append('bnvprotp3')
toberemoved.append('pp')
#toberemoved.append('ep')
#toberemoved.append('mup')
'''

# nmu
toberemoved.append('bnvbcandmass')
toberemoved.append('nbnvbcand')
toberemoved.append('nhighmom')
toberemoved.append('bnvlepp3')
#toberemoved.append('pp')
#toberemoved.append('ep')
toberemoved.append('mup')


# ne
'''
toberemoved.append('bnvbcandmass')
toberemoved.append('nbnvbcand')
#toberemoved.append('tagbcandmass')
toberemoved.append('nhighmom')
toberemoved.append('bnvlepp3')
#toberemoved.append('bnvprotp3')
#toberemoved.append('pp')
toberemoved.append('ep')
#toberemoved.append('mup')
'''

#'''
df = sktools.format(df, className='positive', columns_to_drop=toberemoved)
print(df.columns)

# Get rid of nans
df.dropna(0,inplace=True)
# split into input and output columns
y = df.pop('Class') # all class values become 'y'
X = df
print(len(X))
print(len(y))
# ensure all data are floating point values
X = X.astype('float32')
# encode strings to integer
y = LabelEncoder().fit_transform(y)
# split into train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1) # Save 1 event for the testing part


#df.dropna(0,inplace=True)
#print(len(df))
#X, X_train, X_test, y, y_train, y_test = sktools.preprocess(df, class_string = 'Class', test_size=0.0)

predictions = model.predict(X_train)

np.save('PREDICTIONS_'+datafilename.split('.')[0]+'_'+modelfilename.split('.')[0],predictions)



