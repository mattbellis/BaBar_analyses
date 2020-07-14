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

from matplotlib import pyplot

# **********************************************
# Output: dataset without specified 
#           rows/columns, additional "Class" 
#           column
# **********************************************
def format(df, columnsToDrop, rowsToDrop, className=None):
  df = df.drop(columns=columnsToDrop) # remove specified columns
  df = df.drop(rowsToDrop) # remove specified rows

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


infilenames = sys.argv[1:]


df0,df1 = sktools.read_in_files_and_return_dataframe(infilenames)

print(len(df0),infilenames[0])
print(len(df1),infilenames[1])

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


#df0 = format(df0, ['cos(theta)', 'p3'], 0, 'positive')
#df1 = format(df1, ['cos(theta)', 'p3'], 0, 'negative')
df0 = format(df0, toberemoved, 0, 'positive')
df1 = format(df1, toberemoved, 0, 'negative')
df = mergeDataframes([df0, df1])


# split into input and output columns
y = df.pop('Class') # all class values become 'y'
X = df

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
# evaluate the model
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print('Test Accuracy: %.3f' % acc)

# make a prediction
row = X_test.iloc[[0]] # row/one particle to run prediction on
yhat = model.predict([row]) # makes prediction
print('Predicted: %.3f' % yhat) # 1 = proton, 0 = not proton

model.summary()


# summarize the model
plot_model(model, 'model.png', show_shapes=True)


# plot learning curves
pyplot.title('Learning Curves')
pyplot.xlabel('Epoch')
pyplot.ylabel('Cross Entropy')
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='val')
pyplot.legend()
pyplot.show()

# this curve shows underfitting. How to fix?


