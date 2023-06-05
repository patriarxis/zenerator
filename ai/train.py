import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical

dataset = np.load('datasets/preprocessed_poems.npy', allow_pickle=True).item()
input_sequences = dataset['input_sequences']
output_sequences = dataset['output_sequences']
vocabulary = dataset['vocabulary']

train_size = int(0.8 * len(input_sequences))
train_data = input_sequences[:train_size]
train_labels = output_sequences[:train_size]
val_data = input_sequences[train_size:]
val_labels = output_sequences[train_size:]

vocab_size = len(vocabulary)
embedding_dim = 100
seq_length = len(train_data[0])
num_epochs = 10
batch_size = 32

train_data = [[vocabulary.get(token) for token in poem] for poem in train_data]
train_labels = [vocabulary.get(token) for token in train_labels]
val_data = [[vocabulary.get(token) for token in poem] for poem in val_data]
val_labels = [vocabulary.get(token) for token in val_labels]

train_data = pad_sequences(train_data, maxlen=seq_length, padding='post')
val_data = pad_sequences(val_data, maxlen=seq_length, padding='post')

train_labels = to_categorical(train_labels, num_classes=vocab_size)
val_labels = to_categorical(val_labels, num_classes=vocab_size)

model = Sequential()
model.add(Embedding(input_dim=vocab_size,
          output_dim=embedding_dim, input_length=seq_length))
model.add(LSTM(units=128, return_sequences=True))
model.add(LSTM(units=128))
model.add(Dense(units=vocab_size, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

checkpoint_callback = ModelCheckpoint(
    'models/poetry_model.h5', save_best_only=True)

batch_size = 32
num_batches = int(np.ceil(len(train_data) / batch_size))
for epoch in range(num_epochs):
    for batch in range(num_batches):
        start_idx = batch * batch_size
        end_idx = min((batch + 1) * batch_size, len(train_data))
        batch_data = train_data[start_idx:end_idx]
        batch_labels = train_labels[start_idx:end_idx]

        model.fit(batch_data, batch_labels, epochs=1,
                  batch_size=batch_size, verbose=1)

    loss, accuracy = model.evaluate(val_data, val_labels,
                                    batch_size=batch_size, verbose=0)
    print(
        f'Epoch {epoch+1} - Validation Loss: {loss:.4f} - Validation Accuracy: {accuracy:.4f}')

    model.save_weights(f'models/poetry_model_epoch{epoch+1}.h5')

model.save('models/final_poetry_model.h5')
