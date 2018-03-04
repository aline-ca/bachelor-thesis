#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#                                                                   #
# File:                           evaluate_poems.py                 #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           04/03/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
# Small script for evaluating the rhyme scores of all the           #
# poems in the training data.                                       #
#                                                                   #
#####################################################################

from RhymeEvaluation import Limerick
from RhymeEvaluation import rhyme_evaluation
from pprint import pprint


training_data = rhyme_evaluation.read_in_data('data/training_data.txt')

print('Number of poems: {}'.format(len(training_data)))     # 88682

training_data = rhyme_evaluation.read_in_data('data/training_data.txt')

scores_dict = {}

for i in range(len(training_data)):

    poem = training_data[i]
    current_poem = Limerick.Limerick(poem)

    # Compute current poem score and round up to four decimal points:
    current_score = round(current_poem.get_score(), 4)

    if current_score not in scores_dict:
        scores_dict[current_score] = 1
    else:
        scores_dict[current_score] += 1

pprint(scores_dict)





