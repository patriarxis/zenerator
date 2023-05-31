import random
import nltk
import re
from nltk.corpus import cmudict

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
        word = random.choice(words)
        syllable_count = count_syllables(word)

        if syllable_count <= syllables:
            line.append(word)
            syllables -= syllable_count

    return ' '.join(line)


def generate_haiku_from_text(text_input):
    words = text_input.split()
    haiku = []

    line = generate_line(words, 5)
    haiku.append(line)

    line = generate_line(words, 7)
    haiku.append(line)

    line = generate_line(words, 5)
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
