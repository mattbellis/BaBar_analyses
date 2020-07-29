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

modelfile = sys.argv[1]

model = keras.models.load_model("keras_model")
