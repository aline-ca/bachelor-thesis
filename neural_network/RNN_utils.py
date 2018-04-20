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
import re

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Generates text character-wise based on a trained model. The preset for generated length is 200 chars - 
if an end-of-limerick char occurs in the text, only the string up to this char will be used.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def generate_text(model, length, vocab_size, ix_to_char, char_to_ix):

    generated_text = ['§']                              # Start generation with start-of-limerick sign
    ix_array = [char_to_ix[generated_text[-1]]]         # First entry of index array

    # Create subdictionary only including letters a-z
    # (For the random char that starts the text generation, we only want letters (and not a random space etc.))
    letter_char_to_ix = { key: value for key, value in char_to_ix.items() if key.isalpha() }

    # Create and append random int/char:
    rand_int = [np.random.randint(len(letter_char_to_ix))]
    rand_char = ix_to_char[rand_int[-1]]
    generated_text.append(rand_char)

    X = np.zeros((1, length, vocab_size))           # Create input data X, shape = (1, 200, 32)

    X[0, 0, :][ix_array[-1]] = 1                    # Initialize value for start sign '§' (at position 0)

    ix_array.append(rand_int)                       # Append random char to index array

    # Now predict rest of sequence char by char, based on these two chars (start at 1):
    for i in range(1, length):

        # Note to self: X[i:j:k] means i = starting index, j = stopping index and k = step size
        X[0, i, :][ix_array[-1]] = 1            # Initialize

        # in stateful model, it needs a (seq_length)
        # ValueError: Error when checking : expected lstm_1_input to have shape (50, 71) but got array with shape (1, 71)

        # Predict sequence up to i + 1
        #print(X.shape)
        #geht anscheinend nicht um X.shape, das ist (51, 200, 33) wenn man es ändert

        ix_array = np.argmax(model.predict(X[:, :i + 1, :], verbose=0)[0], 1)

        generated_text.append(ix_to_char[ix_array[-1]])  # Append corresponding char for index

    # Combine generated sequence to string. If an end-of-limerick char was generated, return sequence up to this char,
    # else return the complete sequence. Also remove the start-of-limerick char in the beginning.
    return ''.join(generated_text).split('€')[0][1:]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Method for loading the training data while removing punctuation and digits.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def load_data(data_dir, seq_length):

    data = []
    # Collect and prepare the data as chars:

    with open(data_dir, 'r') as infile:
        for line in infile:
            # Remove all punctuation except: [- ' € § \n|
            line_char_array_1 = re.sub(r"[^\w'\s€§-]+", '', line)
            # Remove digits and underscore:
            line_char_array_2 = list(re.sub(r"[\d_]+", '', line_char_array_1))
            data.extend(line_char_array_2)
    infile.close()

    chars = list(set(data))
    VOCAB_SIZE = len(chars)

    print('Data length: {} characters'.format(len(data)))
    print('Vocabulary size: {} characters'.format(VOCAB_SIZE))

    ix_to_char = {ix: char for ix, char in enumerate(chars)}
    char_to_ix = {char: ix for ix, char in enumerate(chars)}

    num_of_seq = int(len(data) / seq_length)

    X = np.zeros((num_of_seq, seq_length, VOCAB_SIZE))
    y = np.zeros((num_of_seq, seq_length, VOCAB_SIZE))

    for i in range(0, num_of_seq):
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
    return X, y, VOCAB_SIZE, ix_to_char, char_to_ix


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Old method for loading the training data including punctuation and numbers.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def load_data_with_punct(data_dir, seq_length):
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
    return X, y, VOCAB_SIZE, ix_to_char, char_to_ix


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
For a stateful model, the data must be cut at a length so that the number 
of training examples is divisible by the batch size.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_new_data_length(number_of_samples, batch_size):
    return number_of_samples - (number_of_samples % batch_size)


