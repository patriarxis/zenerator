import os
import json
import numpy as np
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from utils.model import create_model

absolute_path = os.path.dirname(__file__)

datasets_path = os.path.join(absolute_path, 'datasets/datasets.npy')
datasets = np.load(datasets_path, allow_pickle=True).item()
train_data = datasets['train_data']
train_labels = datasets['train_labels']
val_data = datasets['val_data']
val_labels = datasets['val_labels']

params_path = os.path.join(absolute_path, 'params.json')
with open(params_path, 'r') as f:
    params = json.load(f)

batch_size = params['batch_size']
dropout = params['dropout']
epochs = params['epochs']

final_model_path = os.path.join(absolute_path, 'models/poetry_model_v2.h5')
best_model = create_model(dropout)
best_model.fit(train_data, train_labels,
               validation_data=(val_data, val_labels),
               callbacks=[ModelCheckpoint(final_model_path, save_best_only=True),
                          EarlyStopping(patience=3)],
               epochs=epochs,
               batch_size=batch_size)

best_model.save(final_model_path)
