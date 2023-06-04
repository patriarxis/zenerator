import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical

dataset = np.load('datasets/preprocessed_haikus.npy', allow_pickle=True).item()
input_sequences = dataset['input_sequences']
output_sequences = dataset['output_sequences']
vocabulary = dataset['vocabulary']

train_size = int(0.8 * len(input_sequences))
train_data = input_sequences[:train_size]
train_labels = output_sequences[:train_size]
val_data = input_sequences[train_size:]
val_labels = output_sequences[train_size:]

train_data = [[vocabulary.get(token) for token in haiku]
              for haiku in input_sequences]
train_labels = [vocabulary.get(token) for token in output_sequences]
val_data = [[vocabulary.get(token) for token in haiku]
              for haiku in input_sequences]
val_labels = [vocabulary.get(token) for token in output_sequences]

vocab_size = len(vocabulary)
embedding_dim = 100
seq_length = len(train_data[0])
num_epochs = 10
batch_size = 32

train_data = pad_sequences(train_data, maxlen=seq_length, padding='post')
train_labels = to_categorical(train_labels, num_classes=vocab_size)
val_data = pad_sequences(val_data, maxlen=seq_length, padding='post')
val_labels = to_categorical(val_labels, num_classes=vocab_size)

print(train_data, '\n')
print(train_labels)

model = Sequential()
model.add(Embedding(input_dim=vocab_size,
          output_dim=embedding_dim, input_length=seq_length))
model.add(LSTM(units=128, return_sequences=True))
model.add(LSTM(units=128))
model.add(Dense(units=vocab_size, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

checkpoint_callback = ModelCheckpoint(
    'models/trained_model.h5', save_best_only=True)

history = model.fit(train_data, train_labels, epochs=num_epochs, batch_size=batch_size,
                    validation_data=(val_data, val_labels), callbacks=[checkpoint_callback])
