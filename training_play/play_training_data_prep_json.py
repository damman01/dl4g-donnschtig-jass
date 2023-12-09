import os
import numpy as np
import pandas as pd
from pathlib import Path
import json
import random
import glob
from jass.game.game_observation import GameObservation
from jass.game.game_state import GameState

from label_play import LabelPlay


def get_train_data(path_to_data):
    print('Searching directory...:', path_to_data)
    files = []
    for file in Path(path_to_data).rglob('*.txt'):
        files.append(file)
    files.sort()
    print('Found {} files.'.format(len(files)))

    data_array = []
    played_card_array = []
    for file_path in files:
        with open(file_path, 'r') as file:
            # Shuffle the lines
            lines_shuffled = file.readlines()
            random.shuffle(lines_shuffled)
            for line in lines_shuffled:
                data = json.loads(line)
                state = GameState.from_json(data.get('obs', {}))
                played_card = data.get('action', {})
                played_card_array.append(played_card)
                label_play = LabelPlay.get_label_play(state, played_card, state.player, state.hands)
                data_array.append(label_play.to_dataframe())
        print("Read in file:", file_path)

    return [data_array, np.array(played_card_array, dtype=np.float32)]
