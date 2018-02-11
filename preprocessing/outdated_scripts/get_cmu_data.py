#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# File:                           get_cmu_data.py                   #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           16/11/17                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#   This script will use the limerick training data and generate    #
#   a file that contains all the text as phonetic representation    #
#   according to the cmu dictionary.                                #
#####################################################################

# Note: This script is out-of-date:

import pronouncing
import itertools
import re
import json

"""
Formatting of the generated file can be read in again very easily with json.load(file)):
Example for formatting of the first poem:
[[["capt'n", 'K AE P T N'],
  ['jack', 'JH AE1 K'],
  ['was', ['W AA1 Z', 'W AA0 Z']],
  ['washed', 'W AA1 SH T'],
  ['over', 'OW1 V ER0'],
  ['the', ['DH AH0', 'DH AH1', 'DH IY0']],
  ['side', 'S AY1 D']],
 [['his', ['HH IH1 Z', 'HH IH0 Z']],
  ['crew', 'K R UW1'],
  ['searched', 'S ER1 CH T'],
  ['but', 'B AH1 T'],
  ['found', 'F AW1 N D'],
  ['not', 'N AA1 T'],
  ['hair', 'HH EH1 R'],
  ['nor', 'N AO1 R'],
  ['hide', 'HH AY1 D']],
 [['no', 'N OW1'],
  ['longer', 'L AO1 NG G ER0'],
  ['the', ['DH AH0', 'DH AH1', 'DH IY0']],
  ['helm', 'HH EH1 L M']],
 [['but', 'B AH1 T'],
  ['the', ['DH AH0', 'DH AH1', 'DH IY0']],
  ['deep', 'D IY1 P'],
  ['benthic', 'B IY AH N TH IH K'],
  ['realm', 'R EH1 L M']],
 [['is', ['IH1 Z', 'IH0 Z']],
  ['where', ['W EH1 R', 'HH W EH1 R']],
  ['jack', 'JH AE1 K'],
  ['will', ['W IH1 L', 'W AH0 L']],
  ['forever', 'F ER0 EH1 V ER0'],
  ['reside', ['R IH0 Z AY1 D', 'R IY0 Z AY1 D']]]]
"""


#######################################################
#                     Functions                       #
#######################################################

# Returns list of all words in the line.
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


"""
  There are a lot of simple compounds that are seperated by one or more '-' characters,
  for example cube-shaped, pizza-man, storm-god etc. and the dictionary should have entries 
  for these simple words. Therefore, split these words at the '-', look up their seperate pronounciations,
  and if prounounciations for all the sub-words were found, combine them.
  Note: Not used right now.
"""
def look_up_compounds(word):
    if "-" in word:
        pronounciations = [pronouncing.phones_for_word(subword) for subword in word.split("-")]
        # If we found one or more pronounciations for every subword, combine them to
        # create the pronounciation of the complete word:
        if [] not in pronounciations:
            combinations = list(itertools.product(*pronounciations))
            pronouncing_list = [('-'.join(combination)) for combination in combinations]
            return pronouncing_list
    return []


def build_unknown_word_dict():
    unknown_word_dict = {}
    with open("unknown_words/unknown_words_complete_dict.txt", 'r') as file:
        for line in file:
            word = line.split(' ', 1)[0]
            # Sometimes there is just one space seperating the word from its pronounciation,
            # and sometimes it's two spaces.
            pronounciation = line.split(' ', 1)[1]
            if pronounciation[0] == ' ':
                pronounciation = pronounciation[1:]

            # Remove newline sign at the end:
            pronounciation = pronounciation[:-1]
            unknown_word_dict[word] = pronounciation

    return unknown_word_dict




# Returns a string representation of the line.
def get_str_repr(words):
    line_without_punctuation = ""
    for word in words:
        if len(line_without_punctuation) == 0:
            line_without_punctuation += word
        else:
            line_without_punctuation += (" " + word)
    return line_without_punctuation


# Get unknown word representation.
def get_unknown_word_repr(word):
    uppercase_word = word.upper()
    if uppercase_word in unknown_word_dict:
        pronouncing_list = unknown_word_dict[uppercase_word]

    else:
        print("word " + word + " still has no pronounciation!")

    return [pronouncing_list]


# Takes the line (punctuation was removed) as list of words as argument and returns a list of its phoneme representations.
# Note: For now, only takes first representation. Still needs mechanism to deal with multiple entries!
def get_phonemes_for_line(words):
    current_words_with_repr = 0
    current_words_without_repr = 0
    current_words_with_mult_repr = 0

    phonemes_for_line = []

    for word in words:

        # CASE 1: Look up whether pronounciation(s) for the complete word exist(s).
        pronouncing_list = get_complete_pronounciation(word)
        # Found pronouncing.
        if pronouncing_list != []:
            # print(word + " " + str(pronouncing_list))

            if len(pronouncing_list) == 1:
                phonemes_for_line.append(pronouncing_list[0])

            if len(pronouncing_list) > 1:
                phonemes_for_line.append([pron for pron in pronouncing_list])


        # If no pronounciation of complete word was found:
        # CASE 2: Look up word in unknown word dict
        else:
            pronouncing_list = get_unknown_word_repr(word)
            # print(word + " " + str(pronouncing_list) + " (unknown word)" )
            phonemes_for_line.append(pronouncing_list[0])

        if pronouncing_list == []:
            current_words_without_repr += 1
        else:
            current_words_with_repr += 1
        if len(pronouncing_list) > 1: current_words_with_mult_repr += 1

    return (phonemes_for_line, current_words_with_repr, current_words_without_repr, current_words_with_mult_repr)


#########################################################################################################

# Open limericks file
with open("data/new_limericks.txt", 'r') as file:
    words_with_repr = 0
    words_without_repr = 0
    words_with_mult_repr = 0

    # Build dictionary with pronouciations for all unknown words (from file generated earlier):
    unknown_word_dict = build_unknown_word_dict()

    all_data = []
    poem_lines = []

    for line in file:

        # If we want no spaces in beetween
        # if line in ['\n', '\r\n']: continue

        # List of words in the line (without punctuation)
        words = parse_line(line)

        # String representation of line
        line_as_str = get_str_repr(words)

        data = get_phonemes_for_line(words)

        phonemes_for_line = data[0]
        current_words_with_repr = data[1]
        current_words_without_repr = data[2]
        current_words_with_mult_repr = data[3]

        assert (len(words) == len(phonemes_for_line)), "Number of words and corresponding phonemes are not the same!"

        words_with_repr += current_words_with_repr
        words_without_repr += current_words_without_repr
        words_with_mult_repr += current_words_with_mult_repr

        # Collect poems into data structure
        if (line_as_str != ""):
            line_data = [(words[i], phonemes_for_line[i]) for i in range(len(words))]
            poem_lines.append(line_data)
        else:
            all_data.append(poem_lines)
            poem_lines = []

    with open('generated_data.txt', 'w') as outfile:
        json.dump(all_data, outfile, indent=2)

    print("Words with representation: " + str(words_with_repr))
    print("Words with multiple representations: " + str(words_with_mult_repr))
    print("Words without representation: " + str(words_without_repr))
    print(str(round((words_without_repr / (
    words_without_repr + words_with_repr) * 100))) + "% of the words in the data have no represenation.")
    print(str(round((words_with_mult_repr / (
    words_without_repr + words_with_repr) * 100))) + "% of the words in the data have multiple represenations.")
