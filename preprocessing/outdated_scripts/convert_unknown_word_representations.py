#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#                                                                   #
# File:                   convert_unknown_word_representations.py   #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           14/12/17                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#####################################################################

import json
import Limerick


########################################################################################################################
input_file  = 'final_generated_data.txt'                  # Read data from this file
output_file = 'new_data_test.txt'                           # Write new data into this file
########################################################################################################################

# Reads in training data from file.
def read_in_data(file):
    with open(file, 'r') as f:
        return json.load(f)


training_data = read_in_data(input_file)
print(len(training_data))

for j in range(len(training_data)):
    poem = training_data[j]
    current_poem = Limerick.Limerick(poem)

    # Iterate over verse positions 0 - 4
    for i in range(len(current_poem.all_verses)):

        #print(i)
        current_verse = current_poem.all_verses[i]
        current_verse_as_str = current_poem.get_verse_as_str(i+1)
        current_unknown_words = current_poem.unknown_words[i]
        current_stress_pattern = current_poem.stress_patterns[i]

        # print(current_verse_as_str)
        # print(current_unknown_words)
        # print(current_stress_pattern)
        # print(current_poem.metres[i])
        # print(current_poem.unknown_words_grids[i])

        assert (len(current_unknown_words)
                == len(current_stress_pattern)), "There is a stress pattern missing."

        # Iterate over representations in data
        verse_in_data = training_data[j][i]
        #print(verse_in_data)

        # Iterate over all words in the verse (in the data)
        for word in verse_in_data:
            word_str = word[0]
            phonemes = word[1]

            # If the word is an unknown word, generate its complete phonetic representation, including stresses.
            if word_str in current_unknown_words:

                index = current_unknown_words.index(word_str)
                #print(current_stress_pattern[index])
                new_repr = current_poem.create_new_repr_for_unknown_word(phonemes, current_stress_pattern[index])

                #print(new_repr)
                #print(training_data[j][i][word])
                index_in_data = training_data[j][i].index(word)

                # Overwrite phonetic representation
                training_data[j][i][index_in_data][1] = new_repr
        #print('\n')

with open(output_file, 'w') as outfile:
    json.dump(training_data, outfile, indent=2)


