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
import random
from keras.preprocessing.sequence import pad_sequences

# Function for sampling the model predictions to a specified temperature.
def sample(preds, temperature=1.0):

    #print("Sampling next character...")

    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)

    #print("Prediction array before multinomial redistribution: ")
    #print(preds)

    probas = np.random.multinomial(1, preds, 1)

    return np.argmax(probas)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Generates text character-wise based on a trained model. 
Uses sampling for specified temperature now.
Preset length is 200 chars -
if an end-of-limerick char occurs in the text, only the string up to this char will be used.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def generate_text(model, length, vocab_size, ix_to_char, char_to_ix, temperature=1.0):

    generated_text = ['§']                              # Start generation with start-of-limerick sign

    for i in range(length):
        sampled = np.zeros((1, length, vocab_size))

        # One-hot encode characters generated so far:
        for t, char in enumerate(generated_text):
            sampled[0, t, char_to_ix[char]] = 1.

        # Predict next character, given the generated text available so far:
        preds = model.predict(sampled[:, :i + 1, :], verbose=0)[0]

        # Returns an array with shape (i, vocab_size) where i corresponds to the current position in the generated
        # sequence. For sampling, we are only interested in the last array that encodes the char probabilities of
        # the current timestep (= next predicted character).
        preds = preds[-1]

        #print("Prediction shape in main function: {}".format(preds.shape))
        #print(preds)

        #print("Current timestep: {} ".format(i))
        #print("Shape of preds: {} ".format(preds.shape))

        next_index = sample(preds, temperature)
        next_char = ix_to_char[next_index]

        #print("Next character: " + next_char)
        #print("Generated text: {}".format(generated_text))

        if next_char == '€':
            generated_text += next_char
            break

        generated_text += next_char

    # Return the complete sequence. Also remove the start-of-limerick char in the beginning.
    #return ''.join(generated_text)[1:]
    return ''.join(generated_text)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Generates text character-wise based on a trained model. The preset for generated length is 200 chars - 
if an end-of-limerick char occurs in the text, only the string up to this char will be used.

METHOD WITHOUT SAMPLING
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def generate_text_old(model, length, vocab_size, ix_to_char, char_to_ix):

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

        ix_array = np.argmax(model.predict(X[:, :i + 1, :], verbose=0)[0], 1)
        print(ix_array)
        print(len(ix_array))


        generated_text.append(ix_to_char[ix_array[-1]])  # Append corresponding char for index

    # Combine generated sequence to string. If an end-of-limerick char was generated, return sequence up to this char,
    # else return the complete sequence. Also remove the start-of-limerick char in the beginning.
    return ''.join(generated_text).split('€')[0][1:]



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Method for loading the training data while removing punctuation and digits.
Uses padding (for stateful=False model)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def load_data_with_padding(data_dir):
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

    ix_to_char = {ix: char for ix, char in enumerate(chars)}
    char_to_ix = {char: ix for ix, char in enumerate(chars)}

    all_sequences = []
    current_sequence = []

    # Collect all single training examples and append them to list:
    for i in range(len(data)):
        if data[i] != '€':
            current_sequence += data[i]
        else:
            current_sequence += data[i]
            all_sequences.append(current_sequence)
            current_sequence = []

    # Save same data with corresponding indices instead of chars:
    all_sequences_as_indices = []
    for i in range(len(all_sequences)):
        current_indices = [int(char_to_ix[value]) for value in all_sequences[i]]
        all_sequences_as_indices.append(current_indices)

    #print(char_to_ix)
    #print(all_sequences[0])
    #print(all_sequences_as_indices[0])

    # Apply padding to sequences:
    padded_sequences = pad_sequences(all_sequences_as_indices, value=99)
    #print(padded_sequences[0])

    assert(len(all_sequences) == len(all_sequences_as_indices) == len(padded_sequences))

    num_of_seq = len(padded_sequences)
    seq_length = len(padded_sequences[0])

    X = np.zeros((num_of_seq, seq_length, VOCAB_SIZE))
    y = np.zeros((num_of_seq, seq_length, VOCAB_SIZE))
    #print(X.shape)

    # Fill training data frame with one-hot encoding of X values:

    # For all training examples:
    for i in range(0, num_of_seq):

        current_sequence = padded_sequences[i]                         # Current sequence values
        input_sequence = np.zeros((seq_length, VOCAB_SIZE))         # Input frame for one-hot encoding

        # For all positions in the current sequence:
        for j in range(seq_length):
            # If we get the padding value 99, do nothing (then the one-hot encoding will be all zeros for this position)
            if current_sequence[j] == 99:
                pass
            else:
                input_sequence[j][current_sequence[j]] = 1        # Create one-hot encoding for current sequence
            X[i] = input_sequence

        # Create target sequence that is shifted by one position compared to current_sequence:
        y_sequence = padded_sequences[i][1:]                # Current training example without first value
        y_sequence = np.append(y_sequence, 99)              # Append padding value at the end (must have same length)

        assert(len(current_sequence) == len(y_sequence))

        target_sequence = np.zeros((seq_length, VOCAB_SIZE))    # Target input frame for one-hot encoding

        # For all positions in the current sequence:
        for j in range(seq_length):
            # If we get the padding value 99, do nothing (then the one-hot encoding will be all zeros for this position)
            if y_sequence[j] == 99:
                pass
            else:
                target_sequence[j][y_sequence[j]] = 1  # Create one-hot encoding for target sequence
            y[i] = target_sequence

        return X, y, VOCAB_SIZE, ix_to_char, char_to_ix


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Method for loading the training data while removing punctuation and digits 
(for stateful=True model)
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
