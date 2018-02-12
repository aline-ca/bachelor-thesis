#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#                                                                   #
# File:                           Limerick.py                       #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           13/12/17                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#####################################################################

import sys
from RhymeEvaluation import vowels


# Limerick class
class Limerick(object):
    def __init__(self, limerick, multi_repr=False):
        self.multi_repr = multi_repr
        # If multiple representations are disabled (by default), only first representation for every word will be used.
        if not self.multi_repr:
            pass
        if len(limerick) == 5:
            # Verses
            self.verse_1 = limerick[0]
            self.verse_2 = limerick[1]
            self.verse_3 = limerick[2]
            self.verse_4 = limerick[3]
            self.verse_5 = limerick[4]
            self.all_verses = [self.verse_1, self.verse_2, self.verse_3, self.verse_4, self.verse_5]

            # Syllable counts for verses
            self.syllable_counts = [self.get_syllable_count_for_verse(i) for i in range(1, 6)]

            # Computed metre for verses (e.g.: "001001001")
            # TODO: If metre becomes None in poem generation, the verse is too long or too short. The script will not
            # TODO: work then. Fix this later by giving a very bad score if the poem does not match the allowed syllable number.
            # TODO: For now, just remove these poems in the training data.
            self.metres = [self.get_metre_for_syllable_count(i) for i in self.syllable_counts]

            # Computed unknown words grid (e.g.: "0X000XXX")
            self.unknown_words_grids = [self.get_unknown_word_grid_for_verse(i) for i in range(1, 6)]

            # List of unknown words in the limerick. Each sublist represents the unknown words in a verse.
            # If a sublist is empty, there are no unknown words in this verse.
            self.unknown_words = [self.get_unknown_words(i) for i in range(1, 6)]

            self.stress_patterns = self.get_stress_pattern_for_unknown_words(self.unknown_words)

        else:
            print("Found limerick that has wrong size: ")
            print(limerick)
            # TODO: Grenzfälle abdecken. Was, wenn Gedicht nicht genau 5 Verse lang ist?  Zeile zu lang etc.


    # Returns the list representation of a verse.
    def get_verse(self, verse_num):
        if verse_num == 1:
            return self.verse_1
        if verse_num == 2:
            return self.verse_2
        if verse_num == 3:
            return self.verse_3
        if verse_num == 4:
            return self.verse_4
        if verse_num == 5:
            return self.verse_5
        else:
            print("Error in get_verse(verse_num): Input number from 1-5 to get corresponding verse of poem.")


    # Returns string representation of verse. Does not include punctuation that was present in the original data.
    def get_verse_as_str(self, verse_num):
        if verse_num == 1:
            verse = self.verse_1
        if verse_num == 2:
            verse = self.verse_2
        if verse_num == 3:
            verse = self.verse_3
        if verse_num == 4:
            verse = self.verse_4
        if verse_num == 5:
            verse = self.verse_5
        if verse_num not in range(1, 6):
            sys.exit("Error in get_verse_as_str(verse_num): Input number from 1-5 to get corresponding verse of poem.")
        line = ""
        for word_repr_pair in verse:
            if len(line) == 0:
                line += word_repr_pair[0]
            else:
                line += (" " + word_repr_pair[0])
        return line


    # Counts the syllables in the phoneme representation of a single word (one vowel = one syllable).
    # TODO: Improve this, does not always work for unknown words (e.g.: 'captn' -> K AE P T N -> actually two syllables)
    def __count_syllables__(self, pron):
        if type(pron) == list:
            pron = pron[0]
        syllable_count = 0
        for phoneme in pron.split():
            if phoneme in vowels.vowels:
                syllable_count += 1
        return syllable_count


    # Counts the syllables of a verse.
    def get_syllable_count_for_verse(self, verse_num):
        if verse_num == 1:
            verse = self.verse_1
        if verse_num == 2:
            verse = self.verse_2
        if verse_num == 3:
            verse = self.verse_3
        if verse_num == 4:
            verse = self.verse_4
        if verse_num == 5:
            verse = self.verse_5
        if verse_num not in range(1, 6):
            sys.exit(
                "Error in get_num_of_syllables_for_verse(verse_num): Input number from 1-5 to get corresponding verse of poem.")

        syllable_count = 0
        for word_repr_pair in verse:
            repr = word_repr_pair[1]
            # If multiple representations are disabled, just use first phoneme representation of word (if there is more than one).
            # TODO: Change something here if mul_repr is enabled.
            if not self.multi_repr and type(repr) == list:
                repr = repr[0]
            syllable_count += self.__count_syllables__(repr)
        return syllable_count


    # Returns a list with five elements that represents the syllable counts of verses 1-5.
    def get_syllable_count_list(self):
        return [self.get_syllable_count_for_verse(i) for i in range(1, 6)]


    # Evaluates whether all verses of the limerick consist of 5 to 11 syllables.
    def has_5_to_11_syllables_per_verse(self):
        for i in self.get_syllable_count_list():
            if i < 5 or i > 11:
                return False
        return True


    # Checks whether a word is an unknown word by looking for unknown vowels in its phoneme representation.
    def is_unknown_word(self, word_pron):
        # Unknown words do not have multiple representations:
        if type(word_pron) == list:
            return False
        for phoneme in word_pron.split():
            if phoneme in vowels.unknown_vowels:
                return True
        return False


    # Checks whether a limerick or a specific verse of a limerick contains an unknown word.
    # No argument: Function will check in the complete limerick and just return True or False.
    # If a number from 1-5 is given as argument, function will only check this verse for unknown words
    # and will also save the unknown words.
    def get_unknown_words(self, verse_num=None):
        unknown_words = []
        # Look in specified verse:
        if verse_num in range(1, 6):
            verse = self.all_verses[verse_num - 1]
            for word_repr_pair in verse:
                if self.is_unknown_word(word_repr_pair[1]):
                    unknown_words.append(word_repr_pair[0])
                    # return True, unknown_words
            # return False, unknown_words
            return unknown_words
        # Look in complete limerick:
        if verse_num is None:
            for verse in self.all_verses:
                for word_repr_pair in verse:
                    if self.is_unknown_word(word_repr_pair[1]):
                        return True
            return False
        else:
            sys.exit(
                "Error in get_unknown_words(verse_num): Input number from 1-5 to get corresponding verse of poem.")


    def get_stress_pattern_for_unknown_words(self, unknown_words):
        stress_patterns = []
        # Iterate over lines and look up corresponding unknown word grid and metre:
        for i in range(1, 6):
            current_grid = self.unknown_words_grids[i - 1]
            current_metre = self.metres[i - 1]
            indices = self.get_position_of_unknown_words(current_grid)
            stress_patterns.append(self.look_up_position_in_metre(current_metre, indices))
        return stress_patterns


    # 0X000000 compute unknown word grid
    def __get_stress_repr_for_word__(self, word_repr_pair):
        stress_repr = ""
        pron = word_repr_pair[1]
        # TODO: Change something here if mul_repr is enabled.
        # For now, just use first representation.
        if type(pron) == list: pron = pron[0]
        if self.is_unknown_word(pron):
            for i in range(0, self.__count_syllables__(pron)):
                stress_repr += "X"
            return stress_repr + ' '
        # Known word
        else:
            # Has one syllable:
            if self.__count_syllables__(pron) == 1:
                return "0"
                # has more than one syllable:
            else:
                for phoneme in pron.split():
                    if phoneme in vowels.vowels:
                        stress_repr += "0"
                return stress_repr


    # Get metre representation for complete verse of a limerick as string.
    def get_unknown_word_grid_for_verse(self, verse_num):
        if verse_num in range(1, 6):
            verse = self.all_verses[verse_num - 1]
            unknown_word_grid = ""
            for word_repr_pair in verse:
                unknown_word_grid += self.__get_stress_repr_for_word__(word_repr_pair)
            return unknown_word_grid
        else:
            sys.exit(
                "Error in get_metre_for_verse(verse_num): Input number from 1-5 to get corresponding verse of poem.")


    def get_metre_for_syllable_count(self, syllable_count):
        if syllable_count == 5:
            return "01001"
        if syllable_count == 6:
            return "001001"  # Nr 2 noch!
        if syllable_count == 7:
            return "0010010"
        if syllable_count == 8:
            return "01001001"
        if syllable_count == 9:
            return "001001001"
        if syllable_count == 10:
            return "0010010010"
        if syllable_count == 11:  # Nr 2 noch!
            return "00100100100"
        else:
            print(syllable_count)
            # Returns None as metre if the verse is too short or long
            sys.exit("Metre in the verse is too short or too long!")
            return None


    # Takes an unknown word grid (e.g. "000X 000XXX") as argument and returns a list of all indices of unknown words
    # in the grid (e.g. [[3], [7, 8, 9]] for the example above)
    def get_position_of_unknown_words(self, unknown_word_grid):

        # The grid includes whitespaces as markers for the end of an unknown word that we do not want to count
        # as indices (because they do not represent a syllable). Therefore, each time we encounter a whitespace
        # we must subtract its position from the index we want to save.
        # e.g.: "XX 00XX 0"  has string length 9, but only 7 syllables. For the second unknown word, we want to
        # return the index [4,5] and not the string index [5,6] that would include the whitespace.
        whitespace_count = 0
        all_positions_list = []
        current_word_positions = []

        # Iterate over all positions in grid:
        for i in range(len(unknown_word_grid)):
            if unknown_word_grid[i] == 'X':
                # Append index for every 'X'
                current_word_positions.append(i - whitespace_count)

                # If the next symbol is a whitespace, we found the complete unknown word:
                if i < len(unknown_word_grid) - 1 and unknown_word_grid[i + 1] == ' ':
                    whitespace_count += 1
                    all_positions_list.append(current_word_positions)
                    current_word_positions = []

                # Special case: The very last symbol is an 'X' (cannot check next position in grid)
                if i == len(unknown_word_grid) - 1 and unknown_word_grid[i] == 'X':
                    all_positions_list.append(current_word_positions)

        return all_positions_list


    # Looks up
    def look_up_position_in_metre(self, metre, unknown_word_indices):
        #print("Looking up metre!")
        all_stresses = []
        for sublist in unknown_word_indices:
            current_stress = ""
            for index in sublist:
                current_stress += metre[index]
            all_stresses.append(current_stress)
        #print("Found following stresses: " + str(all_stresses))

        return all_stresses


    """
    Takes an unknown word, its phonetic representation and its computed stress pattern to iterate through its representation
    and change the vowels from vowels without information to stressed/unstressed vowels, according to the stress pattern.
    Example: word: "mammarially",  representation: "M AA M AH R IY AH L I",  stress pattern "00100"
            -> returns "M AA0 M AH0 R IY1 AH0 L I0"
    """
    def create_new_repr_for_unknown_word(self, representation, stress_pattern):

        new_representation = ""
        current_vowel_position = 0
        stress_positions = [i for i in range(len(stress_pattern)) if stress_pattern[i] == "1"]

        for phoneme in representation.split():
            # If we found a vowel:
            if phoneme in vowels.unknown_vowels:
                if current_vowel_position in stress_positions:  # current vowel is stressed
                    new_representation += phoneme + str(1) + ' '
                    current_vowel_position += 1
                else:  # current vowel is unstressed
                    new_representation += phoneme + str(0) + ' '
                    current_vowel_position += 1
            # If we found a consonant:
            else:
                new_representation += phoneme + ' '

        return new_representation


    # Iterate over
    # Muss auserhalb der Klasse aufgerufen werden.
    def rewrite_unknown_word_repr_in_data(self):
        pass







"""
erstmal nochmal über alles iterieren? Wo wird nach unknown_words abgefragt?
Jetzt nur noch die Repräsentation in den Daten umschreiben! Am Schluss habe ich dann alles in final_generated_data.
"""
