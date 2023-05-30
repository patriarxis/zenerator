import random
import nltk
from nltk.corpus import cmudict

# Download the CMU Pronouncing Dictionary if not already downloaded
nltk.download('cmudict')

# Load the CMU Pronouncing Dictionary
pronouncing_dict = cmudict.dict()


def count_syllables(word):
    # Function to count the number of syllables in a word
    word = word.lower()

    # Check if word is present in the CMU Pronouncing Dictionary
    if word in pronouncing_dict:
        # Each entry in the dictionary represents a list of phonemes for the word
        # Count the number of phonemes that end with a digit, indicating stress
        syllable_count = len(
            [ph for ph in pronouncing_dict[word][0] if ph[-1].isdigit()])
        return syllable_count

    # If word is not found in the dictionary, use a simple fallback method
    # Count the number of vowel sounds (approximation) in the word
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


def generate_haiku_from_text(text_input):
    lines = text_input.split('\n')
    haiku_lines = []
    for line in lines:
        words = line.split()
        syllable_count = sum(count_syllables(word) for word in words)
        haiku_lines.append(words)

        if syllable_count == 5:
            break

    if len(haiku_lines) != 3:
        return None

    haiku = '\n'.join(' '.join(line) for line in haiku_lines)
    return haiku


def generate_haiku_from_code(code):
    lines = code.split('\n')

    # Filter out empty lines and comments
    lines = [line for line in lines if line.strip(
    ) and not line.strip().startswith('#')]

    haiku_lines = []
    syllable_count = 0
    for line in lines:
        words = line.split()
        for word in words:
            syllable_count += count_syllables(word)
        haiku_lines.append(words)

        if syllable_count >= 17:
            break

    if len(haiku_lines) < 3 or syllable_count != 17:
        return None

    haiku = '\n'.join(' '.join(line) for line in haiku_lines[:3])
    return haiku


def generate_haiku(text_input=None, github_repo_url=None):
    if text_input:
        return generate_haiku_from_text(text_input)
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
