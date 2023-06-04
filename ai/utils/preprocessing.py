import string
import numpy as np

padding_token = "<PAD>"


def tokenize_haikus(haikus):
    tokenized_haikus = []
    for haiku in haikus:
        tokens = haiku.split()
        filtered_tokens = [token.strip(string.punctuation) for token in tokens]
        filtered_tokens = [token for token in filtered_tokens if token]
        tokenized_haikus.append(filtered_tokens)
    return tokenized_haikus


def create_vocabulary(tokenized_haikus):
    vocabulary = {}
    for haiku in tokenized_haikus:
        for token in haiku:
            if token not in vocabulary:
                vocabulary[token] = len(vocabulary)
    return vocabulary


def create_sequences(tokenized_haikus, sequence_length):
    input_sequences = []
    output_sequences = []
    for haiku in tokenized_haikus:
        for i in range(len(haiku) - sequence_length):
            input_seq = haiku[i:i+sequence_length]
            output_seq = haiku[i+sequence_length]
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


with open('../datasets/haikus.txt', 'r') as file:
    lines = file.readlines()


haikus = []
current_haiku = []
for line in lines:
    line = line.strip()
    if line == '-' and current_haiku:
        if current_haiku:
            haikus.append(' '.join(current_haiku))
            current_haiku = []
    else:
        current_haiku.append(line)


tokenized_haikus = tokenize_haikus(haikus)
vocabulary = create_vocabulary(tokenized_haikus)

sequence_length = 10
input_sequences, output_sequences = create_sequences(
    tokenized_haikus, sequence_length)
padded_input_sequences = pad_sequences(input_sequences, sequence_length)

preprocessed_data = {
    'input_sequences': padded_input_sequences,
    'output_sequences': output_sequences,
    'vocabulary': vocabulary
}

np.save('../datasets/preprocessed_haikus.npy', preprocessed_data)
