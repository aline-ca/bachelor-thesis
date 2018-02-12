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


"""
Similar phonemes:
vowels:
AA AE AH AO
IH IY
consonants:
P B
T D
K G
M N
S Z
F V
ZH JH

S, Z
V, W
M, N
P, B, T
S, SH
D, T 
"""
def is_similar_vowel(phoneme):
    pass
    # gleichlang
    # über


# ER0    equals    AH0 R (generated for new words)

"""

Perfect rhyme:      return 1            (e.g. leave - achieve) 
Imperfect rhyme:    return 0.9          (e.g. hut - at, wet - said)
ED Distance:
 

"""
def rhymes(repr_1, repr_2):

    # Both representations (words) are different. Collect rhyming parts.
    if repr_1 != repr_2:
        rhyming_parts_1 = {get_rhyming_part(repr) for repr in repr_1}
        rhyming_parts_2 = {get_rhyming_part(repr) for repr in repr_2}

        # Compare rhyming parts.
        # If both rhyming parts are exactly the same, we have a perfect rhyme.
        if rhyming_parts_1 == rhyming_parts_2:
            return 1
        else:
            # If they are not exactly the same, maybe they have one rhyming part in the set that is the same.
            # Therefore intersect the sets.
            s = rhyming_parts_1.intersection(rhyming_parts_2)

            # If the intersection is not empty, we found another perfect rhyme.
            if s != set():
                return 1

            # If the intersection is empty, check for an imperfect rhyme. ED! TODO
            else:

                ed_scores = []
                for repr_1 in rhyming_parts_1:
                    for repr_2 in rhyming_parts_2:
                        ed_scores.append(phonetic_edit_distance.compute_phone_ed(repr_1, repr_2))

                        # return somehow scaled minimum
                        # min(ed_scores)
                return 0

    # If we get here, both phonetic representations are exactly the same.
    # This means that the rhyming part could also be
    #
    # Versuche den Reim-Part der vorherigen Repräsentation zu bilden. Wenn das nicht geht, dann schlechte
    # Score (vermutlich schlecht)
    # we have the same word as rhyme
    else:
         return -1

"""
"""
def evaluate_rhyme(verse_1, verse_2):
    print(current_poem.get_verse_as_str(3))
    print(current_poem.get_verse_as_str(4))

    last_repr_1 = verse_1[-1][1]  # get last representation
    last_repr_2 = verse_2[-1][1]

    # If it is a single string representation, convert to list with string for easier handling.
    if type(last_repr_1) == str:    last_repr_1 = [last_repr_1]
    if type(last_repr_2) == str:    last_repr_2 = [last_repr_2]

    # TODO: Collect cases from rhymes() for score here
    # . . .

    # If we get here, the phonetic representations of the last word in each verse are exactly the same.
    # This could either mean that it's a very bad rhyme (cause using the exact same words is not really rhyming)
    # OR it could actually be a very good rhyme, but the rhyming part extents into the preceding word.
    # One example for such a rhyme:
    # zombies are trying to clutch us  -  run fast so they can't grab or touch us
    if rhymes(last_repr_1, last_repr_2) == -1:
        #print(current_poem.get_verse_as_str(1))
        #print(current_poem.get_verse_as_str(2))
        # print('\n')

        sec_last_repr_1 = verse_1[-2][1]
        sec_last_repr_2 = verse_2[-2][1]

        # If it is a single string representation, convert to list with string for easier handling.
        if type(sec_last_repr_1) == str:    sec_last_repr_1 = [sec_last_repr_1]
        if type(sec_last_repr_2) == str:    sec_last_repr_2 = [sec_last_repr_2]


        #print(rhymes(sec_last_repr_1, sec_last_repr_2))

        if rhymes(sec_last_repr_1, sec_last_repr_2) == -1:

            print(sec_last_repr_1)
            print(sec_last_repr_2)
            print('\n')





#####################################################################


training_data = read_in_data('final_generated_data.txt')
print(len(training_data))       # 88705

for i in range(len(training_data)):

    poem = training_data[i]
    current_poem = Limerick.Limerick(poem)

    #print(current_poem.verse_1)

    evaluate_rhyme(current_poem.verse_3, current_poem.verse_4)

    # Verse 1 + 2
    # last_repr_1 = current_poem.verse_1[-1][1]                 # get last representation
    # last_repr_2 = current_poem.verse_2[-1][1]

    # If it is a single string representation, convert to list with string for easier handling later on.
    # if type(last_repr_1) == str:    last_repr_1 = [last_repr_1]
    # if type(last_repr_2) == str:    last_repr_2 = [last_repr_2]


    # if rhymes(last_repr_1, last_repr_2) == -1:
    #     # print(current_poem.get_verse_as_str(1))
    #     # print(current_poem.get_verse_as_str(2))
    #     # print('\n')
    #
    #     sec_last_repr_1 = current_poem.verse_1[-2][1]
    #     sec_last_repr_2 = current_poem.verse_2[-2][1]

        # print(sec_last_repr_1)
        # print(sec_last_repr_2)

        # call rhyming part + function here now (wie strukturieren??


        #rhyming_part_1 = get_rhyming_part(last_repr_1)
    #print(rhyming_part_1)

    # Verse 2
    #print(current_poem.get_verse_as_str(2))
    #last_repr_2 = current_poem.verse_2[-1][1]  # get last representation

    # Right now just use first representation - Later choose representation that matches better
    #if type(last_repr_2) == list:
     #   last_repr_2 = last_repr_2[0]

    #rhyming_part_2 = get_rhyming_part(last_repr_2)
    #print(rhyming_part_2)