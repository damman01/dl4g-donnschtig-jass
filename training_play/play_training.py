import logging
import os
from pathlib import Path

import pandas as pd
import tensorflow as tf
import tensorflow.keras.mixed_precision as mixed_precision
from keras.callbacks import TensorBoard
from tensorflow import keras

from play_training_data_prep_json import get_train_data


def data_generator(file_list: list):
    for file_name in file_list:
        data = get_train_data(file_name)
        x_train = pd.concat(data[0], ignore_index=True).values
        y_categorical_data_train = keras.utils.to_categorical(data[1])
        print("x_train length:", len(x_train))
        print("y_categorical_data_train length:", len(y_categorical_data_train))
        print("y_categorical_data_train length_shape:", y_categorical_data_train.shape)

        yield x_train, y_categorical_data_train


def train_model(model, data_generator):
    if tf.test.gpu_device_name():
        print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
    else:
        print("Please install GPU version of TF by running  'python3 -m pip install tensorflow[and-cuda]' in your WSL "
              "Environment!")
        raise Exception("Please install GPU version of TF by running  'python3 -m pip install tensorflow[and-cuda]'")

    # open TensorBoard with: 'tensorboard --logdir=logs' in separate terminal
    tb_callback = TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True)

    history = model.fit(
        data_generator,
        steps_per_epoch=len(file_list),
        epochs=10,
        callbacks=[tb_callback]
    )
    return history


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths_to_data = os.path.join(script_dir, "./gamelogs/")
    #paths_to_data = os.path.join(script_dir, "./test_files/")

    # Set up mixed precision
    policy = mixed_precision.Policy('mixed_float16')
    mixed_precision.set_global_policy(policy)

    # Create a MirroredStrategy for distributed training
    if tf.config.list_physical_devices('GPU'):
        strategy = tf.distribute.MirroredStrategy()
    else:
        strategy = None

    # Model creation
    with strategy.scope():
        model = keras.Sequential([
            keras.layers.Dense(154, activation='relu'),
            keras.layers.Dense(310, activation='relu'),
            keras.layers.Dense(620, activation='relu'),
            keras.layers.Dense(1240, activation='relu'),
            keras.layers.Dense(2480, activation='relu'),
            #keras.layers.LeakyReLU(),
            #keras.layers.ELU(alpha=1.0),
            #keras.layers.Dropout(rate=0.1618),
            keras.layers.Dense(1240, activation='relu'),
            keras.layers.Dense(620, activation='relu'),
            keras.layers.Dense(310, activation='relu'),
            keras.layers.Dense(140, activation='relu'),
            keras.layers.Dense(70, activation='relu'),
            keras.layers.Dense(36, activation='softmax')
        ])
        if policy.name == 'mixed_float16':
            model.add(keras.layers.Activation('linear', dtype='float32'))

        model.compile(loss='categorical_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])

    print('Searching directory...:', paths_to_data)
    file_list = []

    for file in Path(paths_to_data).rglob('*.txt'):
        file_list.append(file)
    file_list.sort()
    print('Found {} files.'.format(len(file_list)))

    train_files = file_list[:int(len(file_list) * 0.7)]
    val_files = file_list[int(len(file_list) * 0.8):]
    tes_files = file_list[int(len(file_list) * 0.9):]

    # Create the generators
    train_gen = data_generator(train_files)
    val_gen = data_generator(val_files)

    # Train the model
    history = train_model(model, train_gen)
    logger.info("Trained model with history:")
    logger.info(history)

    # Save the model
    model.save('../models/playModel.keras')

    # Evaluate the model on the validation set
    score = model.evaluate(val_gen, steps=len(val_files))
    logger.info("Evaluation on validation set:")
    logger.info(score)

    # Test the model on new data
    test_files = file_list[int(len(file_list) * 0.8) + 1:]
    test_gen = data_generator(test_files)

    test_loss, test_acc = model.evaluate(test_gen, steps=len(test_files))
    logger.info("Testing on new data:")
    logger.info("Test loss:", test_loss)
    logger.info("Test accuracy:", test_acc)
