#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reformat the poems containing just one word per line. Necessary formatting to check for words in the CMU dictionary
(and also to check for unknown words).
"""

import re

########################################################################################################################
input_file  = 'new_limericks.txt'                       # Read data from this file
output_file = 'limericks_one_word_per_line.txt'         # Write new data into this file
########################################################################################################################


# Returns list of all words in the file.
def parse_line(line):
    # There's a formatting issue with several words in the data. Some of them look like this: "them?let's" because
    # apparently there was no space after the question mark. Therefore, replace question marks inside of words with spaces.
    line = re.sub(r"(?!<=\s)\?(?!=\s)", " ", line, flags=re.U)

    # Remove brackets, punctuation etc at the beginning/end of the word:
    # return [word.strip("?!'\"´,.;:)([]-") for word in line.split()]
    return line.split()


outfile = open(output_file, "w")

# Open limericks file
with open(input_file, 'r') as file:
    for line in file:
        words = parse_line(line)
        for word in words:
            outfile.write(word + "\n")
        outfile.write("\n")
        if line == []: outfile.write("\n")

outfile.close()
