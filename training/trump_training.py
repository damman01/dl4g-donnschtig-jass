import pandas as pd
from pathlib import Path
from tensorflow import keras
import keras.backend as keras_backend

path_to_data = Path('../data/2018_10_18_trump_without_header.csv')
path_to_player_ids = Path('../data/top_third_players.csv')

# Import only a fraction of data for efficient testing
data = pd.read_csv(path_to_data, header=None)
# Import the ids of the best third of players in the dataset.
top_player_ids = pd.read_csv(path_to_player_ids, header=None)

cards = [
# Diamonds
'DA','DK','DQ','DJ','D10','D9','D8','D7','D6',
# Hearts
'HA','HK','HQ','HJ','H10','H9','H8','H7','H6',
# Spades
'SA','SK','SQ','SJ','S10','S9','S8','S7','S6',
# Clubs
'CA','CK','CQ','CJ','C10','C9','C8','C7','C6'
]

# Forehand (yes = 1, no = 0)
forehand = ['FH']

user = ['user']
trump = ['trump']

data.columns = cards + forehand + user + trump

filtered_data = data[data['user'].isin(top_player_ids[0])]

diamonds = filtered_data[['DA','DK','DQ','DJ','D10','D9','D8','D7','D6']]
hearts = filtered_data[['HA','HK','HQ','HJ','H10','H9','H8','H7','H6']]
spades = filtered_data[['SA','SK','SQ','SJ','S10','S9','S8','S7','S6']]
clubs = filtered_data[['CA','CK','CQ','CJ','C10','C9','C8','C7','C6']]
forehand = filtered_data[['FH']]
chosen_trump = filtered_data[['trump']]

number_of_diamonds = diamonds.eq(1).sum(axis=1)
number_of_hearts = hearts.eq(1).sum(axis=1)
number_of_spades = spades.eq(1).sum(axis=1)
number_of_clubs = clubs.eq(1).sum(axis=1)

diamonds_high_cards = diamonds[['DA','DK','DQ','DJ','D10']].eq(1).sum(axis=1)
hearts_high_cards = hearts[['HA','HK','HQ','HJ','H10']].eq(1).sum(axis=1)
spades_high_cards = spades[['SA','SK','SQ','SJ','S10']].eq(1).sum(axis=1)
clubs_high_cards = clubs[['CA','CK','CQ','CJ','C10']].eq(1).sum(axis=1)

diamonds_low_cards = diamonds[['D9','D8','D7','D6']].eq(1).sum(axis=1)
hearts_low_cards = hearts[['H9','H8','H7','H6']].eq(1).sum(axis=1)
spades_low_cards = spades[['S9','S8','S7','S6']].eq(1).sum(axis=1)
clubs_low_cards = clubs[['C9','C8','C7','C6']].eq(1).sum(axis=1)

has_diamonds_buur = diamonds[['DJ']]
has_hearts_buur = hearts[['HJ']]
has_spades_buur = spades[['SJ']]
has_clubs_buur = clubs[['CJ']]

has_diamonds_nell = diamonds[['D9']]
has_hearts_nell = hearts[['H9']]
has_spades_nell = spades[['S9']]
has_clubs_nell = clubs[['C9']]

x_train_trump = pd.concat([
    number_of_diamonds, number_of_hearts, number_of_spades, number_of_clubs,
    diamonds_high_cards, hearts_high_cards, spades_high_cards, clubs_high_cards,
    diamonds_low_cards, hearts_low_cards, spades_low_cards, clubs_low_cards,
    has_diamonds_buur, has_hearts_buur, has_spades_buur, has_clubs_buur,
    has_diamonds_nell, has_hearts_nell, has_spades_nell, has_clubs_nell,
    forehand
], axis=1)

# Assign column names if needed
x_train_trump.columns = [
    'number_of_diamonds', 'number_of_hearts', 'number_of_spades', 'number_of_clubs',
    'diamonds_high_cards', 'hearts_high_cards', 'spades_high_cards', 'clubs_high_cards',
    'diamonds_low_cards', 'hearts_low_cards', 'spades_low_cards', 'clubs_low_cards',
    'has_diamonds_buur', 'has_hearts_buur', 'has_spades_buur', 'has_clubs_buur',
    'has_diamonds_nell', 'has_hearts_nell', 'has_spades_nell', 'has_clubs_nell',
    'forehand'
]


numpy_x_train_trump = x_train_trump.values
numpy_y_train_trump = chosen_trump.values
y_categorical_data_train_trump = keras.utils.to_categorical(numpy_y_train_trump)

def precision(y_true, y_pred):
    true_positives = keras_backend.sum(keras_backend.round(keras_backend.clip(y_true * y_pred, 0, 1)))
    predicted_positives = keras_backend.sum(keras_backend.round(keras_backend.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + keras_backend.epsilon())
    return precision

def recall(y_true, y_pred):
    true_positives = keras_backend.sum(keras_backend.round(keras_backend.clip(y_true * y_pred, 0, 1)))
    possible_positives = keras_backend.sum(keras_backend.round(keras_backend.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + keras_backend.epsilon())
    return recall

def f1_score(y_true, y_pred):
    precision_val = precision(y_true, y_pred)
    recall_val = recall(y_true, y_pred)
    return 2 * ((precision_val * recall_val) / (precision_val + recall_val + keras_backend.epsilon()))


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

history = model.fit(numpy_x_train_trump, y_categorical_data_train_trump, validation_split=0.20, epochs=100, batch_size=20)

model.save('../models/trumpModel.keras')