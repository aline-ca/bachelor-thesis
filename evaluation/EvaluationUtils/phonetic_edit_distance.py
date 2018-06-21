#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#                                                                   #
# File:                           phonetic_edit_distance.py         #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           10/02/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#####################################################################

from EvaluationUtils import phoneme_mapping
import numpy as np

"""
Compute phonetic edit distance between two phonetic representations.
Collect the indices for corresponding phonemes first and then call main function.
"""
def compute_phone_ed(repr_1, repr_2):

    phones_1 = repr_1.split()
    phones_2 = repr_2.split()

    indices_1 = [phoneme_mapping.get_index_for_phoneme(p) for p in phones_1]
    indices_2 = [phoneme_mapping.get_index_for_phoneme(p) for p in phones_2]

    return levenshtein(indices_1, indices_2)


"""
Fast vectorized implementation of levenshtein algorithm.
(Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python)

Modified to use ints instead of chars so that we can use the indices of phonetic symbols for comparison. 
"""
def levenshtein(source, target):
    if len(source) < len(target):
        return levenshtein(target, source)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # Create array from index lists:
    source = np.array(source)
    target = np.array(target)

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
            current_row[1:],
            np.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
            current_row[1:],
            current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]




