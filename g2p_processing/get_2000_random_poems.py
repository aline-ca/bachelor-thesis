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

import random
with open("../data/limericks_with_markers.txt") as f:

    limericks = []
    current_limerick = []
    in_limerick = False

    for line in f:
        if '§' in line:
            in_limerick = True
            continue
        if in_limerick and line not in ['\n', '\r\n'] and '€' not in line:
            current_limerick.append(line.strip('\n'))
        if '€' in line:
            limericks.append(current_limerick)
            current_limerick = []
            in_limerick = False

    print(len(limericks))

    out = open("2000_different_rand_poems.txt", "w")

    all_indices = list(range(0,len(limericks)))

    for i in range(2000):
        # Choose random index from list, remove index from list afterwards.

        random_index = random.choice(all_indices)
        all_indices.remove(random_index)

        for line in limericks[random_index]:
            out.write(line + '\n')
        out.write('\n')

    out.close()
    f.close()

