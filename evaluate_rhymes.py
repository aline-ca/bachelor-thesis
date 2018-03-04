#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#                                                                   #
# File:                           evaluate_rhymes.py                #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           21/02/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
# This script will evaluate all rhymes in the training data by      #
# computing a score for each rhyme and then identifying the         #
# percentage of each score compared to the overall count of rhymes  #
# in the training data.                                             #
#                                                                   #
#####################################################################

from RhymeEvaluation import Limerick
from RhymeEvaluation import rhyme_evaluation

training_data = rhyme_evaluation.read_in_data('data/training_data.txt')

num_of_rhymes = len(training_data) * 4

print('Number of poems: {}'.format(len(training_data)))     # 88682
print('Number of rhymes: {}'.format(num_of_rhymes))

count1_0 = 0
count0_95 = 0
count0_8 = 0
count0_7 = 0
count0_6 = 0
count0_5 = 0
count0_4 = 0
count0_3 = 0
count0_2 = 0
count0_1 = 0
count0_0 = 0

for i in range(len(training_data)):

    poem = training_data[i]
    current_poem = Limerick.Limerick(poem)

    # Verse 1 + 2:
    verse_1_2_score = rhyme_evaluation.rhymes(current_poem.verse_1, current_poem.verse_2)
    if verse_1_2_score == 1:
        count1_0 += 1
    if verse_1_2_score == 0.95:
        count0_95 += 1
    if verse_1_2_score == 0.8:
        count0_8 += 1
    if verse_1_2_score == 0.7:
        count0_7 += 1
    if verse_1_2_score == 0.6:
        count0_6 += 1
    if verse_1_2_score == 0.5:
        count0_5 += 1
    if verse_1_2_score == 0.4:
        count0_4 += 1
    if verse_1_2_score == 0.3:
        count0_3 += 1
    if verse_1_2_score == 0.2:
        count0_2 += 1
    if verse_1_2_score == 0.1:
        count0_1 += 1
    if verse_1_2_score == 0.0:
        count0_0 += 1

    # Verse 3 + 4:
    verse_3_4_score = rhyme_evaluation.rhymes(current_poem.verse_3, current_poem.verse_4)
    if verse_3_4_score == 1:
        count1_0 += 1
    if verse_3_4_score == 0.95:
        count0_95 += 1
    if verse_3_4_score == 0.8:
        count0_8 += 1
    if verse_3_4_score == 0.7:
        count0_7 += 1
    if verse_3_4_score == 0.6:
        count0_6 += 1
    if verse_3_4_score == 0.5:
        count0_5 += 1
    if verse_3_4_score == 0.4:
        count0_4 += 1
    if verse_3_4_score == 0.3:
        count0_3 += 1
    if verse_3_4_score == 0.2:
        count0_2 += 1
    if verse_3_4_score == 0.1:
        count0_1 += 1
    if verse_3_4_score == 0.0:
        count0_0 += 1

    # Verse 1 + 5:
    verse_1_5_score = rhyme_evaluation.rhymes(current_poem.verse_1, current_poem.verse_5)
    if verse_1_5_score == 1:
        count1_0 += 1
    if verse_1_5_score == 0.95:
        count0_95 += 1
    if verse_1_5_score == 0.8:
        count0_8 += 1
    if verse_1_5_score == 0.7:
        count0_7 += 1
    if verse_1_5_score == 0.6:
        count0_6 += 1
    if verse_1_5_score == 0.5:
        count0_5 += 1
    if verse_1_5_score == 0.4:
        count0_4 += 1
    if verse_1_5_score == 0.3:
        count0_3 += 1
    if verse_1_5_score == 0.2:
        count0_2 += 1
    if verse_1_5_score == 0.1:
        count0_1 += 1
    if verse_1_5_score == 0.0:
        count0_0 += 1

    # Verse 2 + 5:
    verse_2_5_score = rhyme_evaluation.rhymes(current_poem.verse_2, current_poem.verse_5)
    if verse_2_5_score == 1:
        count1_0 += 1
    if verse_2_5_score == 0.95:
        count0_95 += 1
    if verse_2_5_score == 0.8:
        count0_8 += 1
    if verse_2_5_score == 0.7:
        count0_7 += 1
    if verse_2_5_score == 0.6:
        count0_6 += 1
    if verse_2_5_score == 0.5:
        count0_5 += 1
    if verse_2_5_score == 0.4:
        count0_4 += 1
    if verse_2_5_score == 0.3:
        count0_3 += 1
    if verse_2_5_score == 0.2:
        count0_2 += 1
    if verse_2_5_score == 0.1:
        count0_1 += 1
    if verse_2_5_score == 0.0:
        count0_0 += 1

print('Percentage of rhymes with...')
print('score 1.0: {}%'.format(round(count1_0/num_of_rhymes, 5)))
print('score 0.95: {}%'.format(round(count0_95/num_of_rhymes, 5)))
print('score 0.8: {}%'.format(round(count0_8/num_of_rhymes, 5)))
print('score 0.7: {}%'.format(round(count0_7/num_of_rhymes, 5)))
print('score 0.6: {}%'.format(round(count0_6/num_of_rhymes, 5)))
print('score 0.5: {}%'.format(round(count0_5/num_of_rhymes, 5)))
print('score 0.4: {}%'.format(round(count0_4/num_of_rhymes, 5)))
print('score 0.3: {}%'.format(round(count0_3/num_of_rhymes, 5)))
print('score 0.2: {}%'.format(round(count0_2/num_of_rhymes, 5)))
print('score 0.1: {}%'.format(round(count0_1/num_of_rhymes, 5)))
print('score 0.0: {}%'.format(round(count0_0/num_of_rhymes, 5)))

# If counts do not add up, something is wrong.
assert(num_of_rhymes == (count1_0 + count0_95 + count0_8 + count0_7 + count0_6 + count0_5 + count0_4 + count0_3 + count0_2 + count0_1 + count0_0))


print("Done!")
