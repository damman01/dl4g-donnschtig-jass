import json
import logging
import os
import numpy as np
import keras.backend as keras_backend
import pandas as pd
from tensorflow import keras
from keras.callbacks import TensorBoard
import tensorflow as tf
from datetime import date
import tensorflow.keras.mixed_precision as mixed_precision

from jass.game.const import team, next_player, same_team
from jass.game.game_state import GameState
from jass.game.game_util import convert_one_hot_encoded_cards_to_str_encoded_list, get_cards_encoded_from_str
from play_training_data_prep_json import get_train_data

if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install GPU version of TF by running  'python3 -m pip install tensorflow[and-cuda]' in your WSL "
          "Environment!")
    raise Exception("Please install GPU version of TF by running  'python3 -m pip install tensorflow[and-cuda]'")

# open TensorBoard with: 'tensorboard --logdir=logs' in separate terminal
tb_callback = TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True)

paths_to_data = "./gamelogs/jass_game_0002/"
#paths_to_data = "./test_files/"

script_dir = os.path.dirname(os.path.abspath(__file__))
data = get_train_data(os.path.join(script_dir, paths_to_data))

x_train = pd.concat(data[0], ignore_index=True)
y_categorical_data_train = keras.utils.to_categorical(data[1])

print("x_train length:", len(x_train))

print("y_categorical_data_train length:", len(y_categorical_data_train))
print("y_categorical_data_train length_shape:", y_categorical_data_train.shape)

# Set up mixed precision
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)

# Create a MirroredStrategy for distributed training
strategy = tf.distribute.MirroredStrategy()

# Model creation
with strategy.scope():
    model = keras.Sequential()
    model.add(keras.layers.Dense(21, activation='relu'))
    model.add(keras.layers.Dense(42, activation='relu'))
    model.add(keras.layers.Dense(84, activation='relu'))
    model.add(keras.layers.Dense(168, activation='relu'))
    model.add(keras.layers.Dense(210, activation='relu'))
    model.add(keras.layers.LeakyReLU())  # Addresses the "dying ReLU" problem by allowing a small gradient for
    # negative inputs, preventing some units from dying during training.
    model.add(keras.layers.ELU(alpha=1.0))  # Smooths the transition for negative inputs, allowing a mean activation
    # closer to zero, which can speed up learning. alpha: float, slope of negative section. Defaults to 1.0.
    model.add(keras.layers.Dropout(rate=0.1618))  # Dropout layers are employed to prevent overfitting in neural
    # networks by randomly setting a fraction of input units to zero during training. The Dropout layer randomly sets
    # input units to 0 with a frequency of rate at each step during training time, which helps prevent overfitting.
    model.add(keras.layers.Dense(140, activation='relu'))
    model.add(keras.layers.Dense(70, activation='relu'))
    model.add(keras.layers.Dense(35, activation='softmax'))
    # If using mixed precision, the final activation should be float32
    if policy.name == 'mixed_float16':
        model.add(keras.layers.Activation('linear', dtype='float32'))

    model.compile(loss='bce',
                  optimizer='sgd',
                  metrics=['accuracy'])

    history = model.fit(x_train, y_categorical_data_train, validation_split=0.20, epochs=10, batch_size=200,
                        callbacks=[tb_callback])

model.save('../models/playModel.keras')
