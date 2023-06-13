import json
import numpy as np
from sklearn.model_selection import GridSearchCV
from scikeras.wrappers import KerasClassifier
from model import model

with open('datasets.json', 'r') as f:
    data_dict = json.load(f)

train_data = np.array(data_dict['train_data'])
train_labels = np.array(data_dict['train_labels'])

with open('params.json', 'r') as f:
    params = json.load(f)

batch_size = params['batch_size']

clf = KerasClassifier(model=model, batch_size=batch_size, verbose=1)

param_grid = dict(
    model__dropout=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    epochs=[5, 10, 15, 20]
)

grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=3)
grid_result = grid_search.fit(train_data, train_labels)

best_params = grid_search.best_params_
dropout = best_params['dropout']
epochs = best_params['epochs']

print("Best Parameters: ", grid_result.best_params_)
print("Best Accuracy: ", grid_result.best_score_)

with open('../params.json', 'r') as f:
    params = json.load(f)

params['dropout'] = dropout
params['epochs'] = epochs

with open('../params.json', 'w') as f:
    json.dump(params, f)
