import random
import nltk
import re
from nltk.corpus import cmudict
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from ai.models import model

nltk.download('cmudict')
pronouncing_dict = cmudict.dict()


def count_syllables(word):
    word = word.lower()
    if word in pronouncing_dict:
        syllable_count = len(
            [ph for ph in pronouncing_dict[word][0] if ph[-1].isdigit()])
        return syllable_count

    vowels = 'aeiouy'
    syllable_count = 0
    prev_char_is_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_is_vowel:
                syllable_count += 1
            prev_char_is_vowel = True
        else:
            prev_char_is_vowel = False

    return syllable_count


def generate_line(words, syllables):
    line = []
    while syllables > 0:
        next_word = model.select_next_word(words, syllables)
        if not next_word:
            break

        syllable_count = model.count_syllables(next_word)

        if syllable_count <= syllables:
            line.append(next_word)
            syllables -= syllable_count

    return ' '.join(line)


def generate_haiku_from_text(text_input):
    generated_text = model.generate(text_input)
    generated_words = word_tokenize(generated_text)
    pos_tags = pos_tag(generated_words)
    relevant_words = [word for word, pos in pos_tags if pos.startswith(
        'N') or pos.startswith('V') or pos.startswith('J')]

    haiku = []

    line = generate_line(relevant_words, 5)
    haiku.append(line)

    line = generate_line(relevant_words, 7)
    haiku.append(line)

    line = generate_line(relevant_words, 5)
    haiku.append(line)

    return '\n'.join(haiku)


def clean_code(code):
    cmu_dict = cmudict.words()
    words = re.findall(r'\b[a-zA-Z]+\b', code)
    readable_words = [word for word in words if len(
        word) > 1 and word.lower() in cmu_dict and word.isalnum()]

    return ' '.join(readable_words)


def generate_haiku_from_code(code):
    cleaned_code = clean_code(code)
    haiku = generate_haiku_from_text(cleaned_code)

    return haiku


def generate_haiku(text_input=None, code_input=None, github_repo_url=None):
    if text_input:
        return generate_haiku_from_text(text_input)
    elif code_input:
        return generate_haiku_from_code(code_input)
    elif github_repo_url:
        # Fetch the GitHub repository and code
        # code = fetch_code_from_github_repo(github_repo_url)

        # For demonstration purposes, generating a random haiku instead
        code = """
        import random
        print(random.randint(1, 10))
        """
        return generate_haiku_from_code(code)
    else:
        return None
