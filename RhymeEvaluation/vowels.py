# Known words: 1 = primary stress, 2 = secondary stress, 0 = unstressed
stressed_vowels = ["AA1", "AE1", "AH1", "AO1", "AW1", "AY1", "EH1", "ER1", "EY1", "IH1", "IY1", "OW1", "OY1", "UH1",
                   "UW1"]
sec_stressed_vowels = ["AA2", "AE2", "AH2", "AO2", "AW2", "AY2", "EH2", "ER2", "EY2", "IH2", "IY2", "OW2", "OY2", "UH2",
                       "UW2"]
unstressed_vowels = ["AA0", "AE0", "AH0", "AO0", "AW0", "AY0", "EH0", "ER0", "EY0", "IH0", "IY0", "OW0", "OY0", "UH0",
                     "UW0"]

# The phonemes in unknown_vowels only occur in unknown words (which have no stress information).
unknown_vowels = ["AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "I", "IY", "OW", "OY", "UH", "UW"]
# 'I' is actually not a valid Arphabet letter, but it gets nevertheless generated for unknown words.

vowels = stressed_vowels + sec_stressed_vowels + unstressed_vowels + unknown_vowels

# A0 gets created as unstressed vowel, maybe add that