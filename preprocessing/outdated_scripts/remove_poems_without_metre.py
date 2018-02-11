#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Small script that removes all poems with verses that contain less than five or more than one syllables
(and therefore cannot be assigned a valid Limerick metric) from the training data.
"""

import json
from vowels import *

########################################################################################################################
input_file  = 'generated_data.txt'                  # Read data from this file
output_file = 'final_generated_data.txt'            # Write new data into this file
########################################################################################################################


# Counts the syllables in the phoneme representation of a single word (one vowel = one syllable).
def count_syllables(pron):
    if type(pron) == list:
        pron = pron[0]
    syllable_count = 0
    for phoneme in pron.split():
        if phoneme in vowels:
            syllable_count += 1
    return syllable_count


# Counts the syllables of a verse.
def get_syllable_count_for_verse(verse):
    syllable_count = 0
    for word_repr_pair in verse:
        representation = word_repr_pair[1]
        if type(representation) == list:
            representation = representation[0]
        syllable_count += count_syllables(representation)
    return syllable_count


# Reads in training data from file.
def read_in_data(file):
    with open(file, 'r') as f:
        return json.load(f)


# Evaluates whether all verses of the limerick consist of 5 to 11 syllables.
def has_5_to_11_syllables_per_verse(syllable_counts):
    for i in syllable_counts:
        if i < 5 or i > 11:
            return False
    return True


training_data = read_in_data(input_file)

print(len(training_data))       # 90409

# Iterate over copy of list and delete the elements from original list
for poem in list(training_data):

    syllable_counts = [get_syllable_count_for_verse(verse) for verse in poem]
    if not has_5_to_11_syllables_per_verse(syllable_counts):
        training_data.remove(poem)

print(len(training_data))       # 88692

with open(output_file, 'w') as outfile:
    json.dump(training_data, outfile, indent=2)
