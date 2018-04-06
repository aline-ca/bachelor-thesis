#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# File:                           LSTM_not_stateful.py              #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           30/03/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#  Modified version of https://github.com/ChunML/text-generator     #
#                                                                   #
#####################################################################

from __future__ import print_function
#import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('TkAgg')
import numpy as np
import time
import csv
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed
import argparse
from RNN_utils import *
from keras import backend as K
import os

# Disable warning "Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

""" 
    BATCH_SIZE:         number of training examples in one forward/backward pass
    LAYER_NUM:          number of hidden layers
    HIDDEN_DIM:         number of neurons in each hidden layer
    EPOCHS:             number of epochs 
    SEQ_LENGTH:         length of training sequence (= time steps) in chars
    GENERATE_LENGTH:    length of generated poem im chars (if no end-of-limerick sign was found)
    WEIGHTS:            for loading weights of a trained model from a HDF5 file
"""
# Parsing arguments for Network
ap = argparse.ArgumentParser()
ap.add_argument('-data_dir', default='data/limericks_with_markers.txt')
ap.add_argument('-batch_size', type=int, default=50)
ap.add_argument('-layer_num', type=int, default=2)
ap.add_argument('-seq_length', type=int, default=50)
ap.add_argument('-hidden_dim', type=int, default=500)
ap.add_argument('-generate_length', type=int, default=200)
ap.add_argument('-epochs', type=int, default=100)
ap.add_argument('-mode', default='train')
ap.add_argument('-weights', default='')

args = vars(ap.parse_args())

BATCH_SIZE = args['batch_size']
LAYER_NUM = args['layer_num']
HIDDEN_DIM = args['hidden_dim']
EPOCHS = args['epochs']
DATA_DIR = args['data_dir']
SEQ_LENGTH = args['seq_length']
GENERATE_LENGTH = args['generate_length']
WEIGHTS = args['weights']


# Creating training data
X, y, VOCAB_SIZE, ix_to_char = load_data(DATA_DIR, SEQ_LENGTH)

# Creating and compiling the Network
model = Sequential()
model.add(LSTM(HIDDEN_DIM, return_sequences=True, input_shape=(None, VOCAB_SIZE)))
# model.add(SimpleRNN(HIDDEN_DIM, return_sequences=True, stateful=True, batch_input_shape=(BATCH_SIZE, SEQ_LENGTH, VOCAB_SIZE)))

for i in range(LAYER_NUM - 1):
  model.add(LSTM(HIDDEN_DIM, return_sequences=True))

model.add(TimeDistributed(Dense(VOCAB_SIZE)))
model.add(Activation('softmax'))
model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

# Generate some sample before training to know how bad it is!
generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)

#from keras.utils import plot_model
#plot_model(model, to_file='model.png', show_shapes=True)

if not WEIGHTS == '':
  model.load_weights(WEIGHTS)
  epochs = int(WEIGHTS[WEIGHTS.rfind('_') + 1:WEIGHTS.find('.')])
else:
    epochs = 0

# Training if there is no trained weights specified
if args['mode'] == 'train' or WEIGHTS == '':
  while True:
    print('\n\nEpoch: {}\n'.format(epochs))
    model.fit(X, y, batch_size=BATCH_SIZE, epochs=EPOCHS)
    epochs += 1
    generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
    if epochs % 10 == 0:
      model.save_weights('checkpoint_layer_{}_hidden_{}_epoch_{}.hdf5'.format(LAYER_NUM, HIDDEN_DIM, epochs))

# Else, loading the trained weights and performing generation only
elif WEIGHTS == '':
  # Loading the trained weights
  model.load_weights(WEIGHTS)
  generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
  print('\n\n')
else:
  print('\n\nNothing to do!')


"""
About every fifth run (pretty randomly) there will be an error message from tensorflow: 
TypeError: 'NoneType' object is not callable
This seems to be a bug - see following issue:
https://github.com/tensorflow/tensorflow/issues/3388
Importing keras backend and clearing the session fixed it for me.
"""
K.clear_session()
