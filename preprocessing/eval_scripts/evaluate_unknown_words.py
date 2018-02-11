#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Short script for counting and evaluating the percentage of unknown words in the data.
"""

import re
import pronouncing

########################################################################################################################
input_file  = 'data/new_limericks.txt'                 # Read data from this file
########################################################################################################################



# Returns list of all words in the file.
def parse_line(line):
    # There's an formatting issue with several words in the data.
    # Some of them look like this: "them?let's" because apparently
    # there was no space after the question mark.
    # Therefore, replace question marks inside of words with spaces.
    line = re.sub(r"(?!<=\s)\?(?!=\s)", " ", line, flags=re.U)

    # Remove brackets, punctuation etc at the beginning/end of the word:
    return [word.strip("?!'\"´,.;:)([]-") for word in line.split()]


# Looks up a complete word in the pronouncing dictionary.
def get_complete_pronounciation(word):
    pronouncing_list = pronouncing.phones_for_word(word)
    if pronouncing_list != []:
        return pronouncing_list
    else:
        return []

    ###################################################################################


# Open limericks file
with open(input_file, 'r') as file:
    poem_lines = []
    poem_counter = 0
    poems_with_unknown_words = 0
    poems_last_word_unknown = 0
    found_unknown_word = False
    last_word_is_unknown_word = False

    for line in file:

        if line not in ['\n', '\r\n']:
            words = parse_line(line)
            poem_lines.append(words)

            for word in words:
                pronouncing_list = get_complete_pronounciation(word)
                if pronouncing_list == []:
                    found_unknown_word = True

        else:

            poem_counter += 1

            if found_unknown_word:
                poems_with_unknown_words += 1

            for line in poem_lines:
                # Get pronounciation of last word for each line:
                pronouncing_list = get_complete_pronounciation(line[-1])

                if pronouncing_list == []:
                    print(line[-1])
                    last_word_is_unknown_word = True

            if last_word_is_unknown_word:
                poems_last_word_unknown += 1

            poem_lines = []
            found_unknown_word = False
            last_word_is_unknown_word = False

    print("There are " + str(poem_counter) + " limericks in the training file.")
    print("There are " + str(poems_with_unknown_words) + " limericks with at least one unknown word.")
    print("There are " + str(poems_last_word_unknown) + " limericks that have an unknown word as last word of a line.")
