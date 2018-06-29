#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
#                                                                   #
# File:                           Limerick.py                       #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           14/06/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#####################################################################

from EvaluationUtils import vowels
from EvaluationUtils import phonetic_edit_distance

"""
EVALUATION CRITERIA:
has_5_verses        [yes/no]
verse_3_4_shorter   [yes/no]
verse_count_score   [1.0 - 0]
metric_score        [1.0 - 0]
rhyme_score         [1.0 - 0]
"""

# Limerick class
class Limerick(object):

    def __init__(self, limerick, phonemes):

        # Lists
        self.verses, self.phonemes = self.__collect_verses_and_phonemes__(limerick, phonemes)  # Verse and phoneme list
        self.syllable_counts = self.__get_syllable_count_list__()                              # List of syllable counts

        # Scores
        self.verse_count_score = self.__evaluate_syllable_counts__()                           # Score for verse counts
        self.metric_score = self.__evaluate_metric_pattern__()                                 # Metric score
        self.rhyme_score = self.__compute_rhyme_score_for_poem__()                             # Rhyme score

        self.verse_3_4_shorter = self.__check_whether_verse_3_4_shorter__()                    # Are verse 3 and 4 shorter?

    def __collect_verses_and_phonemes__(self, limerick, phonemes):
        verses = [verse for verse in limerick]
        phonemes = [phones for phones in phonemes]

        if len(verses) == 5:
            self.has_5_verses = True
        else:
            self.has_5_verses = False

            # If poem is too long, only save first 5 lines:
            if len(verses) > 5:
                verses = verses[:5]
                phonemes = phonemes[:5]

            # If poem is too short, save empty lists as filler for missing verses:
            else:
                no_of_fillers = 5 - len(verses)
                for i in range(no_of_fillers):
                    verses.append([])
                    phonemes.append([])
        return verses, phonemes


    # Counts the syllables in the phoneme representation of a single word (one vowel = one syllable).
    def __count_syllables__(self, pron):
        syllable_count = 0
        for phoneme in pron.split():
            if phoneme in vowels.vowels:
                syllable_count += 1
        return syllable_count


    # Counts the syllables of a verse.
    def __get_syllable_count_for_verse__(self, phonemes):
        syllable_count = 0
        for phone in phonemes:
            syllable_count += self.__count_syllables__(phone)
        return syllable_count


    # Returns a list with five elements that represents the syllable counts of verses 1-5.
    def __get_syllable_count_list__(self):
        return [self.__get_syllable_count_for_verse__(self.phonemes[i]) for i in range(5)]


    """
    Evaluate whether each verse has the allowed number of syllables:
    Verse 1, 2, and 5 can have 8-11 syllables and verse 3, 4: can have 5-7 syllables.
    1.0 = 5/5 syllable counts correct
    0.8 = 4/5 syllable counts correct
    0.6 = 3/5 syllable counts correct
    0.4 = 2/5 syllable counts correct
    0.2 = 1/5 syllable counts correct
    0.0 = 0/5 syllable counts correct
    """
    def __evaluate_syllable_counts__(self):
        errors = 0
        if self.syllable_counts[0] not in (8, 9, 10, 11):
            errors += 1
        if self.syllable_counts[1] not in (8, 9, 10, 11):
            errors += 1
        if self.syllable_counts[2] not in (5, 6, 7):
            errors += 1
        if self.syllable_counts[3] not in (5, 6, 7):
            errors += 1
        if self.syllable_counts[4] not in (8, 9, 10, 11):
            errors += 1

        if errors == 0: return 1.0
        if errors == 1: return 0.8
        if errors == 2: return 0.6
        if errors == 3: return 0.4
        if errors == 4: return 0.2
        if errors == 5: return 0.0


    """
    Evaluate whether each verse fulfils the restrictions of the anapest metre.
    1.0 = 5/5 verses have correct metric pattern 
    0.8 = 4/5 verses have correct metric pattern
    0.6 = 3/5 verses have correct metric pattern
    0.4 = 2/5 verses have correct metric pattern
    0.2 = 1/5 verses have correct metric pattern
    0   = 0/5 verses have correct metric pattern
    """
    def __evaluate_metric_pattern__(self):
        errors = 0
        for i in range(5):      # For all verses

            # Extract all vowels from verse:
            vowel_list = self.__get_vowels_for_verse__(self.phonemes[i])

            # Check whether this verse has the obligatory stresses for anapest metre.
            has_correct_stresses = self.__check_metric_pattern_for_verse__(vowel_list, self.syllable_counts[i])

            if not has_correct_stresses:
                errors += 1

        if errors == 0: return 1.0
        if errors == 1: return 0.8
        if errors == 2: return 0.6
        if errors == 3: return 0.4
        if errors == 4: return 0.2
        if errors == 5: return 0


    # Return list of vowels for the phonetic representation of a verse.
    def __get_vowels_for_verse__(self, phonemes):
        vowel_list = []
        for word_repr in phonemes:
            phone_list = word_repr.split()
            for phoneme in phone_list:
                if phoneme in vowels.vowels:
                    vowel_list.append(phoneme)
        return vowel_list


    # For a verse, check whether it fulfills the restrictions of the anapest metre. Return True if it does, otherwise False.
    def __check_metric_pattern_for_verse__(self, vowel_list, syllable_count):

        # List of syllable positions in verse that have to be stressed (e.g.: [1, 4, 7])
        required_stress_positions = self.__get_required_stress_positions__(syllable_count)

        # Case 1: If the list of syllable positions is empty, the verse does not have 5 to 11 syllables in the line.
        # Return False because this will probably not correspond to a good metre.
        if required_stress_positions == []:
            return False

        # Case 2: We have two possible stress meters for the line (e.g.: [[2, 5], [1, 4]] )
        if len(required_stress_positions) == 2 and isinstance(required_stress_positions[0], (list,)):

            # Check both sublists:
            for sublist in required_stress_positions:
                found_matching_pattern = True

                for stress_pos in sublist:
                    # If we find a position that does not match the restrictions, leave sublist and try the next one.
                    if vowel_list[stress_pos] not in vowels.stressed_vowels:
                        found_matching_pattern = False
                        break

                # If found_matching_pattern was not set to false, we found a matching pattern. Return True.
                if found_matching_pattern:
                    return True
            # If we get here, both sublists did not match the restrictions. Return False.
            return False

        # Case 3: We have exactly one possible stress metre (e.g.: [1, 4, 7])
        else:
            # For every obligatory stress according to anapest metre, check whether the corresponding syllable position
            # in the verse is stressed as well.
            for stress_pos in required_stress_positions:
                if vowel_list[stress_pos] not in vowels.stressed_vowels:
                    return False
        # If we get here, all stresses were correct.
        return True


    # Returns the syllable positions of a verse that need to be stressed for the anapest metre.
    def __get_required_stress_positions__(self, syllable_count):

        if syllable_count == 5:
            # stress pattern: 01001
            return [1,4]

        if syllable_count == 6:
            # stress pattern: 001001 or 010010
            return [[2,5],[1,4]]

        if syllable_count == 7:
            # stress pattern: 0010010
            return [2,5]

        if syllable_count == 8:
            # stress pattern: 01001001
            return [1,4,7]

        if syllable_count == 9:
            # stress pattern: 001001001
            return [2,5,8]

        if syllable_count == 10:
            # stress pattern: 0010010010 or 0100100100
            return [[2,5,8],[1,4,7]]

        if syllable_count == 11:
            # stress pattern: 00100100100
            return [2,5,8]

        else:
            return []


    # Check whether verse 3 and 4 are shorter than all the other verses in the limerick by at least one syllable.
    def __check_whether_verse_3_4_shorter__(self):

        # Check whether verse 3 is at least one syllable shorter than verse 1, 2 and 5:
        if self.syllable_counts[2] + 1 > self.syllable_counts[0]:
            return False
        if self.syllable_counts[2] + 1 > self.syllable_counts[1]:
            return False
        if self.syllable_counts[2] + 1 > self.syllable_counts[4]:
            return False

        # Check whether verse 4 is at least one syllable shorter than verse 1, 2 and 5:
        if self.syllable_counts[3] + 1 > self.syllable_counts[0]:
            return False
        if self.syllable_counts[3] + 1 > self.syllable_counts[1]:
            return False
        if self.syllable_counts[3] + 1 > self.syllable_counts[4]:
            return False
        return True


    """
    Get the rhyming part for the phoneme representation of a word. The rhyming part is defined as everything 
    from the vowel in the stressed syllable nearest the end of the word up to the end of the word.
    
    Source of function: https://github.com/aparrish/pronouncingpy/blob/master/pronouncing/__init__.py#L148 
    """
    def __get_rhyming_part__(self, phones):
        phones_list = phones.split()
        for i in range(len(phones_list) - 1, 0, -1):
            if phones_list[i][-1] in '1':
                return ' '.join(phones_list[i:])
        return phones


    # Computes rhyme score for two phonetic representations.
    def __compute_rhyme_score__(self, phones_1, phones_2):

        # Case 1: Same word. No good rhyme! Return worst score.
        if phones_1 == phones_2:
            return 0.0

        # Case 2: One line missing. Return worst score as well.
        if phones_1 == [] or phones_2 == []:
            return 0.0

        rhyming_part_1 = self.__get_rhyming_part__(phones_1)
        rhyming_part_2 = self.__get_rhyming_part__(phones_2)

        #print("Rhyming part 1: " + str(rhyming_part_1))
        #print("Rhyming part 2: " + str(rhyming_part_2))

        # Case 3: Perfect rhyme. Return best score.
        if rhyming_part_1 == rhyming_part_2:
            return 1.0

        if len(rhyming_part_1) == len(rhyming_part_2):
            # Case 4: Imperfect rhyme. Return best score as well.
            if self.__is_imperfect_rhyme__(rhyming_part_1, rhyming_part_2):
                return 1.0

        # Case 5: Compute score based on phonetic edit distance:
        ed = phonetic_edit_distance.compute_phone_ed(rhyming_part_1, rhyming_part_2)
        #print("rhyming part 1:" + str(rhyming_part_1))
        #print("rhyming part 2:" + str(rhyming_part_2))
        #print("Phone_ED:" + str(ed))
        if ed == 1: return 0.9
        if ed == 2: return 0.8
        if ed == 3: return 0.7
        if ed == 4: return 0.6
        if ed == 5: return 0.5
        if ed == 6: return 0.4
        if ed == 7: return 0.3
        if ed == 8: return 0.2
        if ed == 9: return 0.1
        if ed >= 10: return 0.0


    # Computes a rhyme score for the complete poem by checking the rhymes in all 5 verses.
    def __compute_rhyme_score_for_poem__(self):
        #print("Computing rhyme score for whole poem.")

        if self.has_5_verses:
            score_1_2 = self.__compute_rhyme_score__(self.phonemes[0][-1], self.phonemes[1][-1])

            #print("Computing rhyme score between {} and {}: {}".format(self.phonemes[0][-1], self.phonemes[1][-1], score_1_2))

            score_3_4 = self.__compute_rhyme_score__(self.phonemes[2][-1], self.phonemes[3][-1])
            score_1_5 = self.__compute_rhyme_score__(self.phonemes[0][-1], self.phonemes[4][-1])
            score_2_5 = self.__compute_rhyme_score__(self.phonemes[1][-1], self.phonemes[4][-1])

            return (score_1_2 + score_3_4 + score_1_5 + score_2_5) / 4

            # If we have less than 5 verses in the poem, an empty verse is represented as [].
            # If we try to index the empty list like this, we will receive an IndexError.
            # Hence, check for each score separately and return the worst rhyming score if a verse is empty.
        else:
            try:
                score_1_2 = self.__compute_rhyme_score__(self.phonemes[0][-1], self.phonemes[1][-1])
            except IndexError:
                score_1_2 = 0.0
            try:
                score_3_4 = self.__compute_rhyme_score__(self.phonemes[2][-1], self.phonemes[3][-1])
            except IndexError:
                score_3_4 = 0.0
            try:
                score_1_5 = self.__compute_rhyme_score__(self.phonemes[0][-1], self.phonemes[4][-1])
            except IndexError:
                score_1_5 = 0.0
            try:
                score_2_5 = self.__compute_rhyme_score__(self.phonemes[1][-1], self.phonemes[4][-1])
            except IndexError:
                score_2_5 = 0.0

            return (score_1_2 + score_3_4 + score_1_5 + score_2_5) / 4


    # Function that returns a list of all similar phonemes for a given phoneme.
    def __get_similar_phonemes__(self, phoneme):

        # similar vowels AA, AE, AH, AO, AW
        if phoneme == 'AA': return ['AE', 'AH', 'AO', 'AW']
        if phoneme == 'AA1': return ['AE1', 'AH1', 'AO1', 'AW1']
        if phoneme == 'AE': return ['AA', 'AH', 'AO', 'AW']
        if phoneme == 'AE1': return ['AA1', 'AH1', 'AO1', 'AW1']
        if phoneme == 'AH': return ['AE', 'AA', 'AO', 'AW']
        if phoneme == 'AH1': return ['AE1', 'AA1', 'AO1', 'AW1']
        if phoneme == 'AO': return ['AE', 'AA', 'AH', 'AW']
        if phoneme == 'AO1': return ['AE1', 'AA1', 'AH1', 'AW1']
        if phoneme == 'AW': return ['AE', 'AA', 'AO', 'AH']
        if phoneme == 'AW1': return ['AE1', 'AA1', 'AO1', 'AH1']

        # similar vowels IH, IY
        if phoneme == 'IH': return ['IY']
        if phoneme == 'IH1': return ['IY1']
        if phoneme == 'IY': return ['IH']
        if phoneme == 'IY1': return ['IH1']

        # similar vowels UH, UW
        if phoneme == 'UH': return ['UW']
        if phoneme == 'UH1': return ['UW1']
        if phoneme == 'UW': return ['UH']
        if phoneme == 'UW1': return ['UH1']

        # similar consonants
        if phoneme == 'M': return ['N', 'NG']
        if phoneme == 'N': return ['M', 'NG']
        if phoneme == 'NG': return ['M', 'N']
        if phoneme == 'S': return ['Z']
        if phoneme == 'Z': return ['S']
        if phoneme == 'P': return ['B']
        if phoneme == 'B': return ['P']
        if phoneme == 'T': return ['D', 'DH']
        if phoneme == 'D': return ['T', 'DH']
        if phoneme == 'DH': return ['T', 'D']
        if phoneme == 'K': return ['G']
        if phoneme == 'G': return ['K']
        if phoneme == 'F': return ['V']
        if phoneme == 'V': return ['F']

        # Return empty list if there are no similar phonemes:
        return []


    # Compare the rhyming parts of two words (of same length) to check whether they are identical except for similar
    # phonemes (representing imperfect rhymes).
    # e.g.: ['P', 'AA', 'T'] and ['B', 'AE', 'T'] would be an imperfect rhyme.
    def __is_imperfect_rhyme__(self, repr1, repr2):
        #print("Computing imperfect rhyme. Error occurs here.")
        repr1 = repr1.split()
        repr2 = repr2.split()
        for i in range(len(repr1)):
            # If the phonemes differ at some point, check whether they are similar phonemes.
            if repr1[i] != repr2[i]:
                #print(repr1[i])
                #print(repr2[i])
                similar_phonemes = self.__get_similar_phonemes__(repr1[i])
                if repr2[i] in similar_phonemes:
                    continue
                else:
                    return False
        return True

