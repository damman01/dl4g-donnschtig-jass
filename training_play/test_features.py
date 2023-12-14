import numpy as np

from play_training_data_prep_json import get_train_data

import os
from pathlib import Path
from tensorflow import keras
import pandas as pd


script_dir = os.path.dirname(os.path.abspath(__file__))
paths_to_data = os.path.join(script_dir, "./test_files/")
print('Searching directory...:', paths_to_data)
file_list = []

for file in Path(paths_to_data).rglob('*.txt'):
    file_list.append(file)
file_list.sort()
print('Found {} files.'.format(len(file_list)))

for file_name in file_list:
    data = get_train_data(file_name)
    print("Data From Prep:", data)
    x_train = pd.concat(data[0], ignore_index=True)
    y_categorical_data_train = keras.utils.to_categorical(data[1])
    print("x_train length:", len(x_train))
    print("y_categorical_data_train length:", len(y_categorical_data_train))
    print("y_categorical_data_train length_shape:", y_categorical_data_train.shape)

x_train.to_csv('x_train.csv', index=False)


