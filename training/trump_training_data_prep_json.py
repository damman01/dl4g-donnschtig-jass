import numpy as np
import pandas as pd
from pathlib import Path
import json
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

    paths_to_data = [
        Path('../data/jass_game_0001/jass_game_0001/trump_jass_game_0001_part_0001.txt'),
        Path('../data/jass_game_0002/jass_game_0002/trump_jass_game_0002_part_0001.txt'),
        Path('../data/jass_game_0003/trump_jass_game_0003_part_0001.txt'),
        Path('../data/jass_game_0004/trump_jass_game_0004_part_0001.txt'),
        Path('../data/jass_game_0005/trump_jass_game_0005_part_0001.txt'),
        Path('../data/jass_game_0006/trump_jass_game_0006_part_0001.txt'),
        Path('../data/jass_game_0007/trump_jass_game_0007_part_0001.txt'),
        Path('../data/jass_game_0008/trump_jass_game_0008_part_0001.txt'),
        Path('../data/jass_game_0009/trump_jass_game_0009_part_0001.txt'),
        Path('../data/jass_game_0010/trump_jass_game_0010_part_0001.txt'),
        Path('../data/jass_game_0011/trump_jass_game_0011_part_0001.txt'),
        Path('../data/jass_game_0012/trump_jass_game_0012_part_0001.txt'),
        Path('../data/jass_game_0013/trump_jass_game_0013_part_0001.txt'),
        Path('../data/jass_game_0014/trump_jass_game_0014_part_0001.txt'),
        Path('../data/jass_game_0015/trump_jass_game_0015_part_0001.txt'),
        Path('../data/jass_game_0016/trump_jass_game_0016_part_0001.txt'),
        Path('../data/jass_game_0017/trump_jass_game_0017_part_0001.txt'),
        Path('../data/jass_game_0018/trump_jass_game_0018_part_0001.txt'),
        Path('../data/jass_game_0019/trump_jass_game_0019_part_0001.txt')
    ]

    data_array = []
    trump_array = []
    for path_to_data in paths_to_data:
        with open(path_to_data, 'r') as file:
            for line in file:
                data = json.loads(line)
                obs = GameObservation.from_json(data.get('obs', {}))
                trump_array.append(adjust_trump(data.get('action', {})))
                data_array.append(np.append(obs.hand, adjust_forehand(obs.forehand)))
        print("Read in file: " + path_to_data)
    data = pd.DataFrame(data_array)

    data.columns = get_card_columns() + get_forehand_column()

    x_train_trump = get_features_from_data_frame(data)
    return [x_train_trump, trump_array]

