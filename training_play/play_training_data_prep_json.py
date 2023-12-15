import os
import numpy as np
import pandas as pd
import json
import glob
from jass.game.game_observation import GameObservation
from jass.game.game_state import GameState
from tensorflow import keras

from label_play import LabelPlay


def get_train_data(line):
    data_array = []
    played_card_array = []

    data = json.loads(line)
    state = GameState.from_json(data.get('obs', {}))

    played_card = data.get('action', {})
    played_card_array.append(keras.utils.to_categorical(played_card, num_classes=36))

    label_play = LabelPlay.get_label_play(state, played_card)
    data_array.append(label_play.to_dataframe())

    # Convert the list of DataFrames to a single DataFrame
    data_df = pd.concat(data_array, ignore_index=True)

    # Convert the DataFrame to a numpy array and reshape it to have a shape of (82,)
    data_array = data_df.values.reshape((82,))

    return data_array, played_card_array
