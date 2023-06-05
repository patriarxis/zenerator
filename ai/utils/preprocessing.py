import string
import numpy as np

padding_token = "<PAD>"


def tokenize_poems(poems):
    tokenized_poems = []
    for poem in poems:
        tokens = poem.lower().split()
        filtered_tokens = [token.strip(string.punctuation) for token in tokens]
        filtered_tokens = [token for token in filtered_tokens if token]
        tokenized_poems.append(filtered_tokens)
    return tokenized_poems


def create_vocabulary(tokenized_poems):
    vocabulary = {}
    for poem in tokenized_poems:
        for token in poem:
            if token not in vocabulary:
                vocabulary[token] = len(vocabulary)
    return vocabulary


def create_sequences(tokenized_poems, sequence_length):
    input_sequences = []
    output_sequences = []
    for poem in tokenized_poems:
        for i in range(len(poem) - sequence_length):
            input_seq = poem[i:i+sequence_length]
            output_seq = poem[i+sequence_length]
            input_sequences.append(input_seq)
            output_sequences.append(output_seq)
    print(input_sequences, output_sequences)
    return input_sequences, output_sequences


def pad_sequences(sequences, max_sequence_length):
    padded_sequences = []
    for sequence in sequences:
        if len(sequence) < max_sequence_length:
            sequence = sequence + [padding_token] * \
                (max_sequence_length - len(sequence))
        else:
            sequence = sequence[:max_sequence_length]
        padded_sequences.append(sequence)
    return padded_sequences


with open('../datasets/poems.txt', 'r') as file:
    lines = file.readlines()


poems = []
current_poem = []
for line in lines:
    line = line.strip()
    if line == '-' and current_poem:
        if current_poem:
            poems.append(' '.join(current_poem))
            current_poem = []
    else:
        current_poem.append(line)


tokenized_poems = tokenize_poems(poems)
vocabulary = create_vocabulary(tokenized_poems)

sequence_length = 10
input_sequences, output_sequences = create_sequences(
    tokenized_poems, sequence_length)
padded_input_sequences = pad_sequences(input_sequences, sequence_length)

preprocessed_data = {
    'input_sequences': padded_input_sequences,
    'output_sequences': output_sequences,
    'vocabulary': vocabulary
}

print(vocabulary)

np.save('../datasets/preprocessed_poems.npy', preprocessed_data)
