#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# File:                           STATEFUL_LSTM.py                  #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           15/04/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#  Modified version of https://github.com/ChunML/text-generator     #
#                                                                   #
#####################################################################

from __future__ import print_function
import os
import argparse
#import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('TkAgg')
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.callbacks import History
from keras import backend as K
from RNN_utils import *
from datetime import datetime

# Disable warning "Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

""" 
    BATCH_SIZE:         number of training examples in one forward/backward pass
    LAYER_NUM:          number of hidden layers
    HIDDEN_DIM:         number of neurons in each hidden layer
    EPOCHS:             number of epochs 
    SEQ_LENGTH:         length of training sequence (= time steps) in chars
    GENERATE_LENGTH:    length of generated poem im chars (if no end-of-limerick sign was found)
    ID:                 A string that can be specified by hand to describe the model, for example 'model_1' or 
                        'stateless_lstm_1'. The saved weights and logfile will then be named after this id string.  
"""
# Parsing arguments for Network
ap = argparse.ArgumentParser()
ap.add_argument('-training_data_dir', default='data/limericks_with_markers.txt')
ap.add_argument('-batch_size', type=int, default=50)
ap.add_argument('-layer_num', type=int, default=2)
ap.add_argument('-seq_length', type=int, default=400)
ap.add_argument('-hidden_dim', type=int, default=500)
ap.add_argument('-generate_length', type=int, default=200)
ap.add_argument('-epochs', type=int, default=200)
ap.add_argument('-id', type=str, default='model_1')

args = vars(ap.parse_args())

BATCH_SIZE = args['batch_size']
LAYER_NUM = args['layer_num']
HIDDEN_DIM = args['hidden_dim']
EPOCHS = args['epochs']
TRAIN_DATA_DIR = args['training_data_dir']
SEQ_LENGTH = args['seq_length']
GENERATE_LENGTH = args['generate_length']
ID = args['id']

#####################################################################

this_filename = os.path.basename(__file__)
time = datetime.now().strftime('%d-%m-%Y-%H:%M')

# Create logfile
logfile = open(ID + '_LOGFILE.txt',"w")

# Write some information and model specifications into logfile:
logfile.write('FILE NAME: {}\n'.format(this_filename))
logfile.write('MODEL ID STRING: {}\n'.format(ID))
logfile.write('MODEL STARTED AT: {}\n\n'.format(time))

logfile.write('MODEL PARAMETERS\n')
logfile.write('BATCH SIZE: {}\n'.format(BATCH_SIZE))
logfile.write('HIDDEN LAYERS: {}\n'.format(LAYER_NUM))
logfile.write('NEURONS PER LAYER: {}\n'.format(HIDDEN_DIM))
logfile.write('TRAINING SEQUENCE LENGTH: {}\n\n'.format(SEQ_LENGTH))

logfile.write('OTHER KERAS TRAINING PARAMETERS:\n')
logfile.write('stateful = True\n')
logfile.write('shuffle = False\n\n')

# Create directory where weights should be saved:
weight_dir = ID + '_WEIGHTS'
if not os.path.exists(weight_dir):
    os.makedirs(weight_dir)

#####################################################################

# Creating training data
X, y, VOCAB_SIZE, ix_to_char, char_to_ix = load_data(TRAIN_DATA_DIR, SEQ_LENGTH)

# For stateful model, cut X and y at a length so that the number of training examples is divisible by batch size:
new_length = get_new_data_length(len(X), BATCH_SIZE)

X = X[:new_length]
y = y[:new_length]

logfile.write('Vocabulary size (Total number of different chars): {}\n'.format(VOCAB_SIZE))
logfile.write('Number of training examples: {}\n\n\n'.format(len(X)))


# MODEL FOR TRAINING (stateful=True):
train_model = Sequential()
train_model.add(LSTM(HIDDEN_DIM, return_sequences=True, stateful=True, batch_input_shape=(BATCH_SIZE, SEQ_LENGTH, VOCAB_SIZE)))

for i in range(LAYER_NUM - 1):
    train_model.add(LSTM(HIDDEN_DIM, return_sequences=True))

train_model.add(TimeDistributed(Dense(VOCAB_SIZE)))
train_model.add(Activation('softmax'))
train_model.compile(loss="categorical_crossentropy", optimizer="rmsprop")


# MODEL FOR PREDICTING (stateful=False):
predict_model = Sequential()
predict_model.add(LSTM(HIDDEN_DIM, return_sequences=True, input_shape=(None, VOCAB_SIZE)))

for j in range(LAYER_NUM - 1):
    predict_model.add(LSTM(HIDDEN_DIM, return_sequences=True))

predict_model.add(TimeDistributed(Dense(VOCAB_SIZE)))
predict_model.add(Activation('softmax'))
predict_model.compile(loss="categorical_crossentropy", optimizer="rmsprop")


train_model.save_weights(weight_dir + '/weights_epoch_{}.hdf5'.format(0))
predict_model.load_weights(weight_dir + '/weights_epoch_{}.hdf5'.format(0))

# Generate some sample text before starting the training:
sample_text = generate_text(predict_model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char, char_to_ix)
print(sample_text)

logfile.write('Epoch: 0 (random generation before training)\n')
logfile.write(sample_text + '\n')

current_epoch = 1
history = History()         # for getting the loss as number (not just printed to console)


#####################################################################

# Run model for specified number of epochs (default = 200 epochs)
while current_epoch <= EPOCHS:

  print('\n\nEpoch: {}\n'.format(current_epoch))
  logfile.write('\n\nEpoch: {}\n'.format(current_epoch))

  # Train model for one epoch, then generate some text, then continue training, and so on.
  hist = train_model.fit(X, y, batch_size=BATCH_SIZE, shuffle=False, epochs=1, callbacks=[history])
  # (Note: Need to define callbacks if we want to extract the loss to write it into logfile.)

  #train_model.save_weights('lstm_model_test.h5')
  #predict_model.load_weights('lstm_model_test.h5')
  train_model.save_weights(weight_dir + '/weights_epoch_{}.hdf5'.format(current_epoch))
  predict_model.load_weights(weight_dir + '/weights_epoch_{}.hdf5'.format(current_epoch))

  generated_text = generate_text(predict_model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char, char_to_ix)
  print('\n\n' + generated_text)

  logfile.write(generated_text + '\n\n')

  loss = round(hist.history['loss'][0], 6)
  logfile.write("Loss: {} \n".format(str(loss)))

  current_epoch += 1


logfile.close()

"""
About every fifth run (pretty randomly) there will be an error message from tensorflow: 
TypeError: 'NoneType' object is not callable
This seems to be a bug - see following issue:
https://github.com/tensorflow/tensorflow/issues/3388
Importing keras backend and clearing the session fixed it for me.
"""
K.clear_session()
