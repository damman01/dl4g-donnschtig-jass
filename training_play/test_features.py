import numpy as np

from play_training_data_prep_json import get_train_data

import os
from pathlib import Path
from tensorflow import keras
import pandas as pd
from keras.src.utils.np_utils import to_categorical

script_dir = os.path.dirname(os.path.abspath(__file__))
paths_to_data = os.path.join(script_dir, "./test_files/small/")
print('Searching directory...:', paths_to_data)
file_list = []

for file in Path(paths_to_data).rglob('*.txt'):
    file_list.append(file)
file_list.sort()
print('Found {} files.'.format(len(file_list)))

for file_name in file_list:
    with open(file_name, 'r') as file:
        print("\nReading file:", file_name)
        lines = file.readlines()
        x_train = []
        for line in lines:
            data = get_train_data(line)
            print("Data From Prep:", data)
            x_train.append(data[0])
            y_categorical_data_train = data[1]
            print("x_train length:", len(x_train))
            print("y_categorical_data_train length:", len(y_categorical_data_train))
            print("y_categorical_data_train length_shape:", y_categorical_data_train.shape)

# Convert the x_train list to a DataFrame
x_train_df = pd.DataFrame(x_train)

# Save the DataFrame to a CSV file
x_train_df.to_csv('x_train.csv', index=False)


