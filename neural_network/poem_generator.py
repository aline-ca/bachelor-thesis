#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# File:                           poem_generator.py                 #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           12/07/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#####################################################################

from __future__ import print_function
import os
import argparse
import matplotlib as mpl
mpl.use('TkAgg')
from RNN_utils import *
from keras.models import load_model
from keras import backend as K
import sys

"""  
    EXAMPLE FUNCTION CALLS:
    
    Load model and generate default number of poems with default temperature:
    python poem_generator.py saved_model.hdf5 
    
    Load model and generate 10 poems with temperature 1.0:
    python poem_generator.py saved_model.hdf5 -temperature 1.0 -poems 1 0
    
"""

# Disable warning "Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#######################################################################################################################

# Deterministic char mapping that is used during every training process:

ix_to_char = {0: '\t', 1: '\n', 2: ' ', 3: "'", 4: '-', 5: 'a', 6: 'b', 7: 'c', 8: 'd', 9: 'e', 10: 'f', 11: 'g',
              12: 'h', 13: 'i', 14: 'j', 15: 'k', 16: 'l', 17: 'm', 18: 'n', 19: 'o', 20: 'p', 21: 'q', 22: 'r',
              23: 's', 24: 't', 25: 'u', 26: 'v', 27: 'w', 28: 'x', 29: 'y', 30: 'z', 31: '§', 32: '€'}

char_to_ix = {'x': 28, 't': 24, 'w': 27, "'": 3, 'l': 16, 'y': 29, 'm': 17, 'f': 10, 'a': 5, 'q': 21, 'e': 9,
              'u': 25, 'b': 6, 'g': 11, 'j': 14, 'n': 18, '\n': 1, 'r': 22, 'p': 20, 'h': 12, 'k': 15, 'z': 30,
              '-': 4, 'd': 8, ' ': 2, 'v': 26, 'o': 19, 'c': 7, '\t': 0, 'i': 13, 's': 23, '§': 31, '€': 32}

VOCAB_SIZE = len(ix_to_char)

#######################################################################################################################

# Parse command line arguments:
ap = argparse.ArgumentParser()
ap.add_argument('filename')
ap.add_argument('-temperature', type=float, default=0.5)
ap.add_argument('-poems', type=int, default=5)
args = vars(ap.parse_args())

TEMPERATURE = args['temperature']
NUM_OF_POEMS = args['poems']

try:
    # Load prediction model
    model = load_model(sys.argv[1])
except OSError:
    print("Cannot open file '" + sys.argv[1] + "'. Please specify a saved model in .hdf5 format.")
    exit()

for i in range(NUM_OF_POEMS):
    generated_text = generate_text(model, 200, VOCAB_SIZE, ix_to_char, char_to_ix, temperature = TEMPERATURE)
    print(generated_text)


"""
About every fifth run (pretty randomly) there will be an error message from tensorflow: 
TypeError: 'NoneType' object is not callable
This seems to be a bug - see following issue:
https://github.com/tensorflow/tensorflow/issues/3388
Importing keras backend and clearing the session fixed it for me.
"""
K.clear_session()