import numpy as np
import pandas as pd
from pathlib import Path
import json
import glob
from jass.game.game_observation import GameObservation

from training.trump_features import get_features_from_data_frame, get_card_columns, get_forehand_column


def adjust_trump(trump_selection):
    if trump_selection == 10:
        return 6
    else:
        return trump_selection

def adjust_forehand(forehand_from_json):
    # Forehand (yes = 1, no = 0)
    if forehand_from_json == -1:
        return 1
    else:
        return 0


def get_train_data():

    #paths_to_data = "./gamelogs/"
    paths_to_data = "./test_files/"

    print('Searching directory...')
    files = glob.glob(paths_to_data, recursive=True)
    files.sort()
    print('Found {} files.'.format(len(files)))

    data_array = []
    trump_array = []
    for file_path in files:
        with open(file_path, 'r') as file:
            for line in file:
                data = json.loads(line)
                obs = GameObservation.from_json(data.get('obs', {}))
                trump_array.append(adjust_trump(data.get('action', {})))
                data_array.append(np.append(obs.hand, adjust_forehand(obs.forehand)))
        print("Read in file:", file_path)
    data = pd.DataFrame(data_array)

    data.columns = get_card_columns() + get_forehand_column()

    x_train_trump = get_features_from_data_frame(data)
    return [x_train_trump, trump_array]

