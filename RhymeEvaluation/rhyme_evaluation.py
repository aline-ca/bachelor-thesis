#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#                                                                   #
# File:                           rhyme_evaluation.py               #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           21/02/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
# Includes all functions that are necessary for evaluating          #
# the quality of a rhyme.                                           #
#####################################################################

import json
from RhymeEvaluation import phonetic_edit_distance

"""
Reads in training data from file. 
"""
def read_in_data(file):
    with open(file, 'r') as f:
        return json.load(f)


"""
Get the rhyming part for the phoneme representation of a word. The rhyming part is defined as everything from the vowel 
in the stressed syllable nearest the end of the word up to the end of the word.

Source of function: https://github.com/aparrish/pronouncingpy/blob/master/pronouncing/__init__.py#L148 
"""
def get_rhyming_part(phones):
    phones_list = phones.split()
    for i in range(len(phones_list) - 1, 0, -1):
        if phones_list[i][-1] in '12':
            return ' '.join(phones_list[i:])
    return phones

"""
Checks the rhyming part of two representations.
Returns TRUE if we found a perfect rhyme.
Returns FALSE if the phonetic representations of the words are exactly the same.
"""
def has_same_rhyming_part(repr_1, repr_2):

    # Both representations (words) are different. Collect rhyming parts.
    if repr_1 != repr_2:
        rhyming_parts_1 = {get_rhyming_part(repr) for repr in repr_1}
        rhyming_parts_2 = {get_rhyming_part(repr) for repr in repr_2}

        # Compare rhyming parts.
        # If both rhyming parts are exactly the same, we have a perfect rhyme.
        if rhyming_parts_1 == rhyming_parts_2:
            return True
        else:
            # If they are not exactly the same, maybe they have one rhyming part in the set that is the same.
            # Therefore intersect the sets.
            s = rhyming_parts_1.intersection(rhyming_parts_2)

            # If the intersection is not empty, we found another perfect rhyme.
            if s != set():
                return True
    # If we get here, both phonetic representations are exactly the same.
    else:
        return False


# Collect pre-defined score for phonetic edit distance calculation. Scores can later be adjusted/tuned if necessary.
def get_score_for_ed(ed):
    if ed == 0:
        return 0
    if ed == 1:
        return 0.95
    if ed == 2:
        return 0.8
    if ed == 3:
        return 0.7
    if ed == 4:
        return 0.6
    if ed == 5:
        return 0.5
    if ed == 6:
        return 0.4
    if ed == 7:
        return 0.3
    if ed == 8:
        return 0.2
    if ed == 9:
        return 0.1
    if ed > 9:
        return 0

"""
Checks whether two verses rhyme.
Look up in documentation for a detailed description on the scores.
"""
def rhymes(verse_1, verse_2):

    # Case 1: Both verses are exactly the same, so it's not a rhyme. Return worst score.
    if verse_1 == verse_2:
        return 0

    last_repr_1 = verse_1[-1][1]  # Get representation of last word in the verse.
    last_repr_2 = verse_2[-1][1]

    assert((len(last_repr_1)) > 0), print(verse_1)
    assert((len(last_repr_2)) > 0), print(verse_2)

    # If it is a single string representation, convert to list with string for easier handling.
    if type(last_repr_1) == str:    last_repr_1 = [last_repr_1]
    if type(last_repr_2) == str:    last_repr_2 = [last_repr_2]

    # Both representations (words) are different. Check whether they have the same rhyming part.
    if last_repr_1 != last_repr_2:

        # Compare rhyming parts.
        # If both rhyming parts are exactly the same, we have a perfect rhyme. Return best score.
        if has_same_rhyming_part(last_repr_1, last_repr_2):
            return 1

    # If we get here, the phonetic representations of the last word in each verse are exactly the same.
    # This could actually be a very good rhyme if the rhyming part extents into the preceding word.
    # One example for such a rhyme:
    # zombies are trying to clutch us  -  run fast so they can't grab or touch us
    else:
        if len(verse_1) > 1 and len(verse_2) > 1:

            sec_last_repr_1 = verse_1[-2][1]        # Get representation of second last word in the verse.
            sec_last_repr_2 = verse_2[-2][1]

            # If it is a single string representation, convert to list with string for easier handling.
            if type(sec_last_repr_1) == str:    sec_last_repr_1 = [sec_last_repr_1]
            if type(sec_last_repr_2) == str:    sec_last_repr_2 = [sec_last_repr_2]

            # Both representations (words) are different. Check whether they have the same rhyming part.
            if sec_last_repr_1 != sec_last_repr_2:

                # Compare rhyming parts.
                # If both rhyming parts are exactly the same, we have a perfect rhyme. Return best score.
                if has_same_rhyming_part(sec_last_repr_1, sec_last_repr_2):
                    return 1

            # If we get here, the phonetic representations of the last and second last word in each verse are the same.
            # This could still be a very good rhyme if the rhyming part extents into the preceding word.
            # One example for such a rhyme:
            # every choice from the start of it - cuz the much better part of it
            else:
                if len(verse_1) > 2 and len(verse_2) > 2:

                    third_last_repr_1 = verse_1[-3][1]  # Get representation of third last word in the verse.
                    third_last_repr_2 = verse_2[-3][1]

                    # If it is a single string representation, convert to list with string for easier handling.
                    if type(third_last_repr_1) == str:    third_last_repr_1 = [third_last_repr_1]
                    if type(third_last_repr_2) == str:    third_last_repr_2 = [third_last_repr_2]

                    # Both representations (words) are different. Check whether they have the same rhyming part.
                    if third_last_repr_1 != third_last_repr_2:

                        # Compare rhyming parts.
                        # If both rhyming parts are exactly the same, we have a perfect rhyme. Return best score.
                        if has_same_rhyming_part(third_last_repr_1, third_last_repr_2):
                            return 1

    # If we get here, we did not find a perfect rhyme.
    # Instead compute phonetic edit distances for the rhyming parts of all possible representations.
    ed_scores = []
    rhyming_parts_1 = {get_rhyming_part(repr) for repr in last_repr_1}
    rhyming_parts_2 = {get_rhyming_part(repr) for repr in last_repr_2}
    for repr_1 in rhyming_parts_1:
        for repr_2 in rhyming_parts_2:
            ed_scores.append(phonetic_edit_distance.compute_phone_ed(repr_1, repr_2))
    best_ed = min(ed_scores)                # Get best ed
    return get_score_for_ed(best_ed)        # Collect predefined score for ed

