#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mapping of arphabet symbols to numbers (for easier handling and efficiency reasons)
"""

phoneme_list = ['AA', 'AA1', 'AE', 'AE1', 'AH', 'AH1', 'AO', 'AO1', 'AW', 'AW1', 'AY', 'AY1', 'EH', 'EH1', 'ER', 'ER1',
                'EY', 'EY1', 'IH', 'IH1', 'IY', 'IY1', 'OW', 'OW1', 'OY', 'OY1', 'UH', 'UH1', 'UW', 'UW1', 'B', 'CH', 'D',
                'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']

def get_index_for_phoneme(phoneme):
    assert(phoneme in phoneme_list), "Phoneme '{}' does not have an index!".format(phoneme)
    return phoneme_list.index(phoneme)

def get_phoneme_for_index(index):
    assert(index < len(phoneme_list)), "Index '{}' does not have a corresponding phoneme!".format(index)
    return phoneme_list[index]