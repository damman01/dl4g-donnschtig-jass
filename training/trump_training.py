import keras.backend as keras_backend
from tensorflow import keras
import tensorflow

from training.trump_training_data_prep_csv import get_train_data as get_train_data_from_csv
from training.trump_training_data_prep_json import get_train_data as get_train_data_from_json

# data = get_train_data_from_csv()
data = get_train_data_from_json()

x_train_trump = data[0]
y_categorical_data_train_trump = keras.utils.to_categorical(data[1])

print(len(x_train_trump))
print(len(y_categorical_data_train_trump))

# Model creation
model = keras.Sequential()
model.add(keras.layers.Dense(21, activation='relu'))
model.add(keras.layers.Dense(42, activation='relu'))
model.add(keras.layers.Dense(84, activation='relu'))
model.add(keras.layers.Dense(168, activation='relu'))
model.add(keras.layers.Dense(210, activation='relu'))
model.add(keras.layers.LeakyReLU()) #Addresses the "dying ReLU" problem by allowing a small gradient for negative inputs, preventing some units from dying during training.
model.add(keras.layers.ELU(alpha=1.0)) # Smooths the transition for negative inputs, allowing a mean activation closer to zero, which can speed up learning. alpha: float, slope of negative section. Defaults to 1.0.
model.add(keras.layers.Dropout(rate=0.1618)) #Dropout layers are employed to prevent overfitting in neural networks by randomly setting a fraction of input units to zero during training. The Dropout layer randomly sets input units to 0 with a frequency of rate at each step during training time, which helps prevent overfitting.
model.add(keras.layers.Dense(140, activation='relu'))
model.add(keras.layers.Dense(70, activation='relu'))
model.add(keras.layers.Dense(7, activation='softmax'))
model.compile(loss='bce',
              optimizer='sgd',
              metrics=['accuracy'])

history = model.fit(x_train_trump, y_categorical_data_train_trump, validation_split=0.20, epochs=10, batch_size=20)

model.save('../models/trumpModel.keras')