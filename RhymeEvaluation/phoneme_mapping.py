
"""
Mapping of the CMU dictionary phoneme symbols to numbers (for easier handling and efficiency reasons)

Note: Added 'TS' ans 'IX' as phonemes. Not valid arphabet symbols, but still get generated for unknown word pronunciations.

"""


phoneme_list = ['AA', 'AA0', 'AA1', 'AA2', 'AE', 'AE0', 'AE1', 'AE2', 'AH', 'AH0', 'AH1', 'AH2', 'AO', 'AO0', 'AO1', 'AO2', 'AW', 'AW0', 'AW1', 'AW2', 'AY', 'AY0', 'AY1', 'AY2', 'B', 'CH', 'D', 'DH', 'EH', 'EH0', 'EH1', 'EH2', 'ER', 'ER0', 'ER1', 'ER2', 'EY', 'EY0', 'EY1', 'EY2', 'F', 'G', 'HH', 'IH', 'IH0', 'IH1', 'IH2', 'IY', 'IY0', 'IY1', 'IY2', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OW0', 'OW1', 'OW2', 'OY', 'OY0', 'OY1', 'OY2', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 'UH0', 'UH1', 'UH2', 'UW', 'UW0', 'UW1', 'UW2', 'V', 'W', 'Y', 'Z', 'ZH', 'TS', 'IX']

def get_index_for_phoneme(phoneme):
    assert(phoneme in phoneme_list), "Phoneme '{}' does not have an index!".format(phoneme)
    return phoneme_list.index(phoneme)

def get_phoneme_for_index(index):
    assert(index < len(phoneme_list)), "Index '{}' does not have a corresponding phoneme!".format(index)
    return phoneme_list[index]