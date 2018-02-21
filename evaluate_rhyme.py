#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#                                                                   #
# File:                           evaluate_rhyme.py                  #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           7/02/18                           #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#####################################################################

import json
from RhymeEvaluation import Limerick
from RhymeEvaluation import phonetic_edit_distance

"""
Reads in training data from file. 
"""
def read_in_data(file):
    with open(file, 'r') as f:
        return json.load(f)


"""
Get the rhyming part for the phoneme representation of a word. The rhyming part is defined as everything from the vowel in the stressed
syllable nearest the end of the word up to the end of the word.

Source of function: https://github.com/aparrish/pronouncingpy/blob/master/pronouncing/__init__.py#L148 
"""
def get_rhyming_part(phones):
    phones_list = phones.split()
    for i in range(len(phones_list) - 1, 0, -1):
        if phones_list[i][-1] in '12':
            return ' '.join(phones_list[i:])
    return phones


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


"""
Checks whether two verses rhyme.
Case 1: Both verses are exactly the same, so it's not a rhyme. Return worst score.
Perfect rhyme:      return 1            (e.g. leave - achieve) 

ED Distance:
"""
def rhymes_2(verse_1, verse_2):

    # Case 1: Both verses are exactly the same, so it's not a rhyme. Return worst score.
    if verse_1 == verse_2:
        return -1

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

    # If we get here:
    ed_scores = []
    rhyming_parts_1 = {get_rhyming_part(repr) for repr in last_repr_1}
    rhyming_parts_2 = {get_rhyming_part(repr) for repr in last_repr_2}
    for repr_1 in rhyming_parts_1:
        for repr_2 in rhyming_parts_2:
            ed_scores.append(phonetic_edit_distance.compute_phone_ed(repr_1, repr_2))

    return(min(ed_scores))


#####################################################################


#training_data = read_in_data('../data/training_data.txt')
training_data = read_in_data('data/training_data.txt')

print(len(training_data))       # 88705

for i in range(len(training_data)):

    poem = training_data[i]
    current_poem = Limerick.Limerick(poem)


    if rhymes_2(current_poem.verse_1, current_poem.verse_2) == 4:
        print(current_poem.get_verse_as_str(1))
        print(current_poem.get_verse_as_str(2))
        print(rhymes_2(current_poem.verse_1, current_poem.verse_2))
        print('\n')

print("Done!")
