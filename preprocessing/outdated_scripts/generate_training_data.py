#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# File:                           generate_training_data.py         #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           11/02/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#   This script will read in limericks from the .txt file and       #
#   collect or generate phonetic representations for all occurring  #
#   words (including stress of unknown words). It will also filter  #
#   out training examples that do not have 5-11 syllables per       #
#   verse.                                                          #
#   The resulting training data is written in a specified output    #
#   file in a convenient formatting (see below for an example).     #
#                                                                   #
#####################################################################

"""
This script combines the functionality of the three following separate scripts:
        get_cmu_data.py
        remove_poems_without_metre.py
        convert_unknown_word_representations.py
Note that the other scripts are outdated and should not be used anymore.
"""

import pronouncing
import re
import json
from RhymeEvaluation import Limerick
from RhymeEvaluation import vowels

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

########################################################################################################################
input_file          = 'data/limericks.txt'                                      # Read data from this file
output_file         = 'data/training_data.txt'                                  # Write new data into this file
unknown_word_dict   = 'unknown_words/unknown_words_complete_dict.txt'           # Location of unknown words dictionary
########################################################################################################################


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
    stripped_line = [word.strip("?!'\"´,.;:)([]-") for word in line.split()]

    # Remove all empty strings from list (they get created for single dots in the data, e.g. in a line like this:
    # you're home, without question . . .)
    while '' in stripped_line:
        stripped_line.remove('')

    return stripped_line


# Looks up a complete word in the pronouncing dictionary.
def get_complete_pronunciation(word):
    pronouncing_list = pronouncing.phones_for_word(word)
    if pronouncing_list:
        return pronouncing_list
    else:
        return []


def build_unknown_word_dict():
    unknown_word_dict = {}
    with open("unknown_words/unknown_words_complete_dict.txt", 'r') as file:
        for line in file:
            word = line.split(' ', 1)[0]
            # Sometimes there is just one space seperating the word from its pronunciation,
            # and sometimes it's two spaces.
            pronunciation = line.split(' ', 1)[1]
            if pronunciation[0] == ' ':
                pronunciation = pronunciation[1:]

            # Remove newline sign at the end:
                pronunciation = pronunciation[:-1]
            unknown_word_dict[word] = pronunciation

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
        print("word " + word + " still has no pronunciation!")

    return [pronouncing_list]


# Takes the line (punctuation was removed) as list of words as argument and returns a list of its phoneme representations.
# Note: For now, only takes first representation. Still needs mechanism to deal with multiple entries!
def get_phonemes_for_line(words):

    phonemes_for_line = []

    for word in words:

        # CASE 1: Look up whether pronunciation(s) for the complete word exist(s).
        pronouncing_list = get_complete_pronunciation(word)
        # Found pronouncing.
        if pronouncing_list != []:

            if len(pronouncing_list) == 1:
                phonemes_for_line.append(pronouncing_list[0])

            if len(pronouncing_list) > 1:
                phonemes_for_line.append([pron for pron in pronouncing_list])

        # If no pronunciation of complete word was found:
        # CASE 2: Look up word in unknown word dict
        else:
            pronouncing_list = get_unknown_word_repr(word)
            phonemes_for_line.append(pronouncing_list[0])
    return phonemes_for_line


# Reads in training data from file.
def read_in_data(file):
    with open(file, 'r') as f:
        return json.load(f)


# Counts the syllables in the phoneme representation of a single word (one vowel = one syllable).
def count_syllables(pron):
    if type(pron) == list:
        pron = pron[0]
    syllable_count = 0
    for phoneme in pron.split():
        if phoneme in vowels.vowels:
            syllable_count += 1
    return syllable_count


# Counts the syllables of a verse.
def get_syllable_count_for_verse(verse):
    syllable_count = 0
    for word_repr_pair in verse:
        representation = word_repr_pair[1]
        if type(representation) == list:
            representation = representation[0]
        syllable_count += count_syllables(representation)
    return syllable_count


# Evaluates whether all verses of the limerick consist of 5 to 11 syllables.
def has_5_to_11_syllables_per_verse(syllable_counts):
    for i in syllable_counts:
        if i < 5 or i > 11:
            return False
    return True


########################################################################################################################


with open(input_file, 'r') as infile:                       # Open limericks file

    # Build dictionary with pronunciations for all unknown words (from file generated earlier):
    unknown_word_dict = build_unknown_word_dict()

    all_data = []           # Complete data frame
    poem_lines = []         # All verses of current poem

    for line in infile:
        # If we want no spaces in beetween
        # if line in ['\n', '\r\n']: continue

        words = parse_line(line)                                # List of words in the line (without punctuation)

        line_as_str = get_str_repr(words)                       # String representation of line
        phonemes_for_line = get_phonemes_for_line(words)        # Phoneme representation of line

        assert (len(words) == len(phonemes_for_line)), "Number of words and corresponding phonemes are not the same!"

        if line_as_str != "":
            # Create data structure for current verse:
            line_data = [(words[i], phonemes_for_line[i]) for i in range(len(words))]
            poem_lines.append(line_data)                 # Append current verse to poem representation

        else:       # If we found an empty line, the current poem is over.

            # Part 2: Count syllables in each verse of the current poem. We only want to save the poem if each verse
            # has at least five, but not more than 11 syllables (otherwise we cannot assign a valid limerick metric).
            syllable_counts = [get_syllable_count_for_verse(verse) for verse in poem_lines]
            if has_5_to_11_syllables_per_verse(syllable_counts):

                # Part 3: Convert the phonetic representations of unknown words (so far, they do not contain any
                # information about stress). Extract the stress patterns of the complete verse to guess the stress
                # corresponding unknown words.
                current_poem = Limerick.Limerick(poem_lines)        # Create Limerick class instance

                for i in range(len(current_poem.all_verses)):       # Iterate over verse positions 0 - 4
                    current_verse = current_poem.all_verses[i]
                    current_verse_as_str = current_poem.get_verse_as_str(i + 1)
                    current_unknown_words = current_poem.unknown_words[i]
                    current_stress_pattern = current_poem.stress_patterns[i]

                    assert (len(current_unknown_words)
                            == len(current_stress_pattern)), "There is a stress pattern missing."

                    # Iterate over representations in data:
                    verse_in_data = poem_lines[i]

                    # Iterate over all words in the verse (in the data)
                    for word in verse_in_data:
                        word_str = word[0]
                        phonemes = word[1]

                        # If word is unknown word, generate its complete phonetic representation, including stresses.
                        if word_str in current_unknown_words:
                            index = current_unknown_words.index(word_str)
                            new_repr = current_poem.create_new_repr_for_unknown_word(phonemes,
                                                                                     current_stress_pattern[index])

                            index_in_data = poem_lines[i].index(word)

                            # Overwrite phonetic representation

                            # Convert tuple to list because tuples are immutable. Change value and convert back to list.
                            # (Pretty ugly, but it works. Maybe change this later)
                            poem_lines[i][index_in_data] = list(poem_lines[i][index_in_data])
                            poem_lines[i][index_in_data][1] = new_repr
                            poem_lines[i][index_in_data] = tuple(poem_lines[i][index_in_data])

                all_data.append(poem_lines)   # Append complete poem representation to overall data structure
            poem_lines = []

    print("Generated data frame and collected stresses for unknown words.")
    print("Total number of poems: " + str(len(all_data)))                           # 88692
    print("Writing data into file '" + output_file + "' now...")

    with open(output_file, 'w') as outfile:
        json.dump(all_data, outfile, indent=2)
        outfile.close()

infile.close()

print("Done!")
