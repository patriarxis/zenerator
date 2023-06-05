from nltk.corpus import cmudict


class ZeneratorAI:
    def __init__(self):
        self.pronouncing_dict = cmudict.dict()

    def select_next_word(self, words, syllables):
        best_word = None
        best_syllable_diff = float('inf')

        for word in words:
            syllable_count = self.count_syllables(word)
            syllable_diff = abs(syllable_count - syllables)

            if syllable_diff < best_syllable_diff:
                best_word = word
                best_syllable_diff = syllable_diff

        return best_word
