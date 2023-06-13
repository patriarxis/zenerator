import os
import json
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

absolute_path = os.path.dirname(__file__)

preprocessed_poems_path = os.path.join(
    absolute_path, '../datasets/preprocessed_poems.npy')
dataset = np.load(preprocessed_poems_path,
                  allow_pickle=True).item()
input_sequences = dataset['input_sequences']
output_sequences = dataset['output_sequences']
vocabulary = dataset['vocabulary']

params_path = os.path.join(absolute_path, '../params.json')
with open(params_path, 'r') as f:
    params = json.load(f)

vocab_size = len(vocabulary)
seq_length = len(input_sequences[0])
embedding_dim = params['embedding_dim']


def seperate_dataset_training_and_validation():
    train_size = int(0.8 * len(input_sequences))
    train_data = input_sequences[:train_size]
    train_labels = output_sequences[:train_size]
    val_data = input_sequences[train_size:]
    val_labels = output_sequences[train_size:]

    train_data = [[vocabulary.get(token) for token in poem]
                  for poem in train_data]
    train_labels = [vocabulary.get(token) for token in train_labels]
    val_data = [[vocabulary.get(token) for token in poem] for poem in val_data]
    val_labels = [vocabulary.get(token) for token in val_labels]

    train_data = pad_sequences(train_data, maxlen=seq_length, padding='post')
    val_data = pad_sequences(val_data, maxlen=seq_length, padding='post')

    train_labels = to_categorical(train_labels, num_classes=vocab_size)
    val_labels = to_categorical(val_labels, num_classes=vocab_size)

    return train_data, train_labels, val_data, val_labels


glove_embeddings_path = os.path.join(
    absolute_path, '../glove/glove_embeddings.npy')


def calculate_embedding_weights_with_glove():
    embedding_matrix = np.load(glove_embeddings_path, allow_pickle=True)
    embedding_weights = np.zeros((vocab_size, embedding_dim))

    for i, word in enumerate(vocabulary):
        embedding_vector = embedding_matrix[i]
        if embedding_vector is not None:
            embedding_weights[i] = embedding_vector

    return embedding_weights


train_data, train_labels, val_data, val_labels = seperate_dataset_training_and_validation()
datasets = {
    'train_data': train_data,
    'train_labels': train_labels,
    'val_data': val_data,
    'val_labels': val_labels
}

datasets_path = os.path.join(absolute_path, '../datasets/datasets.npy')
np.save(datasets_path, datasets)

params['vocab_size'] = vocab_size
params['seq_length'] = seq_length

with open('../params.json', 'w') as f:
    json.dump(params, f)

embedding_weights = calculate_embedding_weights_with_glove()
embedding_weights_data = {
    'embedding_weights': embedding_weights
}

embedding_weights_path = os.path.join(
    absolute_path, '../glove/embedding_weights.npy')
np.save(embedding_weights_path, embedding_weights_data)
