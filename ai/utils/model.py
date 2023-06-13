import os
import json
import numpy as np
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

absolute_path = os.path.dirname(__file__)

params_path = os.path.join(absolute_path, '../params.json')
with open(params_path, 'r') as f:
    params = json.load(f)

vocab_size = params['vocab_size']
seq_length = params['seq_length']
batch_size = params['batch_size']
embedding_dim = params['embedding_dim']
units = params['units']

embedding_weights_file = os.path.join(
    absolute_path, '../glove/embedding_weights.npy')
glove_weights = np.load(embedding_weights_file,
                        allow_pickle=True).item()
embedding_weights = glove_weights['embedding_weights']


def create_model(dropout):
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size,
                        output_dim=embedding_dim,
                        weights=[embedding_weights],
                        input_length=seq_length,
                        trainable=False))
    model.add(LSTM(units=units, return_sequences=True))
    model.add(Dropout(dropout))
    model.add(LSTM(units=units, return_sequences=False))
    model.add(Dropout(dropout))
    model.add(Dense(units=vocab_size, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    return model
