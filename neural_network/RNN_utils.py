#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# File:                           RNN_utils.py                      #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           26/03/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#   Modified version of https://github.com/ChunML/text-generator    #
#                                                                   #
#####################################################################

import numpy as np

"""
Generates text character-wise based on a trained model.
The preset for generated length is 200 chars - if an end-of-limerick char occurs in the text,
only the string up to this char will be used.
"""
def generate_text(model, length, vocab_size, ix_to_char):

    ix = [np.random.randint(vocab_size)]    # Start with random character (as int)
    y_char = [ix_to_char[ix[-1]]]           # Get char from int
    X = np.zeros((1, length, vocab_size))   # Create input data X, shape = (1,200,71)

    # Iterate over generated length (step by step, to predict single chars):
    for i in range(length):
        # Appending the last predicted character to sequence
        X[0, i, :][ix[-1]] = 1      # Init
        # print(ix_to_char[ix[-1]], end="")

        # ValueError: Error when checking : expected lstm_1_input to have shape (50, 71) but got array with shape (1, 71)

        ix = np.argmax(model.predict(X[:, :i + 1, :], verbose=0)[0], 1)
        y_char.append(ix_to_char[ix[-1]]) # Append corresponding char for index
    # Combine generated sequence to string. If an end-of-limerick char was generated, return sequence up to this char,
    # else return the complete sequence.
    return''.join(y_char).split('€')[0]


# method for preparing the training data
def load_data(data_dir, seq_length):
    data = open(data_dir, 'r').read()
    chars = list(set(data))
    VOCAB_SIZE = len(chars)

    print('Data length: {} characters'.format(len(data)))
    print('Vocabulary size: {} characters'.format(VOCAB_SIZE))

    ix_to_char = {ix: char for ix, char in enumerate(chars)}
    char_to_ix = {char: ix for ix, char in enumerate(chars)}

    X = np.zeros((int(len(data) / seq_length), seq_length, VOCAB_SIZE))
    y = np.zeros((int(len(data) / seq_length), seq_length, VOCAB_SIZE))
    for i in range(0, int(len(data) / seq_length)):
        X_sequence = data[i * seq_length:(i + 1) * seq_length]
        X_sequence_ix = [char_to_ix[value] for value in X_sequence]
        input_sequence = np.zeros((seq_length, VOCAB_SIZE))
        for j in range(seq_length):
            input_sequence[j][X_sequence_ix[j]] = 1.
            X[i] = input_sequence

        y_sequence = data[i * seq_length + 1:(i + 1) * seq_length + 1]
        y_sequence_ix = [char_to_ix[value] for value in y_sequence]
        target_sequence = np.zeros((seq_length, VOCAB_SIZE))
        for j in range(seq_length):
            target_sequence[j][y_sequence_ix[j]] = 1.
            y[i] = target_sequence
    return X, y, VOCAB_SIZE, ix_to_char
