import os
from pathlib import Path
from pandas import DataFrame, concat
from play_training_data_prep_json import get_train_data

script_dir = os.path.abspath(os.path.dirname(__file__))
paths_to_data = os.path.join(script_dir, "./test_files/small/")
print('Searching directory...:', paths_to_data)

file_list = sorted(Path(paths_to_data).rglob('*.txt'))
print('Found {} files.'.format(len(file_list)))

x_train = DataFrame()
for file_name in file_list:
    print("\nReading file:", file_name)
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data = get_train_data(line)
            print("Data From Prep data[0]:", data[0])
            print("Data From Prep data[1]:", data[1])
            print("Data From Prep Type:", type(data[0]))
            x_train = concat([x_train, DataFrame(data[0])])            

            y_categorical_data_train = DataFrame(data[1])
            print("x_train length:", len(x_train))
            print("x_train length_shape:", x_train.shape)
            print("y_categorical_data_train length:", len(y_categorical_data_train))
            print("y_categorical_data_train length_shape:", y_categorical_data_train.shape)
# 
# Save the DataFrame to a CSV file
x_train.to_csv('x_train.csv', index=False)


