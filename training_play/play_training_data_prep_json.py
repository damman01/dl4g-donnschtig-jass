import numpy as np
from pandas import DataFrame, concat
import json
from jass.game.game_state import GameState
from tensorflow import keras
from label_play import LabelPlay


def get_train_data(line) -> (DataFrame, DataFrame):
    """
    This function takes a line of JSON data and returns the training data and the label data.
    :param line:
    :return:
    """
    data = json.loads(line)
    state = GameState.from_json(data.get('obs', {}))
    played_card = data.get('action', {})

    played_card_array = keras.utils.to_categorical(played_card, num_classes=36)
    label_play = LabelPlay.get_label_play(state, played_card)

    return get_data_from_labelplay(label_play), played_card_array


def get_data_for_play(line) -> np.ndarray:
    """
    This function takes a line of JSON data and returns the training data and the label data.
    :param line:
    :return:
    """
    data = json.loads(line)
    state = GameState.from_json(data.get('obs', {}))

    label_play = LabelPlay.get_label_play(state, -1)

    return get_data_from_labelplay(label_play)


def get_data_from_labelplay(label_play):
    data_frame = label_play.to_dataframe()
    feature_ranges = dict(points_in_trick_own=(0, 50), points_in_trick_other=(0, 50), trick_winner=(0, 3),
                          points_in_game_own=(0, 151), points_in_game_other=(0, 151), declared_trump=(0, 3),
                          trump=(0, 5), forehand=(0, 1), nr_tricks=(0, 8), nr_cards_in_trick=(0, 3), hand_card_0=(0, 1),
                          hand_card_1=(0, 1), hand_card_2=(0, 1), hand_card_3=(0, 1), hand_card_4=(0, 1),
                          hand_card_5=(0, 1), hand_card_6=(0, 1), hand_card_7=(0, 1), hand_card_8=(0, 1),
                          hand_card_9=(0, 1), hand_card_10=(0, 1), hand_card_11=(0, 1), hand_card_12=(0, 1),
                          hand_card_13=(0, 1), hand_card_14=(0, 1), hand_card_15=(0, 1), hand_card_16=(0, 1),
                          hand_card_17=(0, 1), hand_card_18=(0, 1), hand_card_19=(0, 1), hand_card_20=(0, 1),
                          hand_card_21=(0, 1), hand_card_22=(0, 1), hand_card_23=(0, 1), hand_card_24=(0, 1),
                          hand_card_25=(0, 1), hand_card_26=(0, 1), hand_card_27=(0, 1), hand_card_28=(0, 1),
                          hand_card_29=(0, 1), hand_card_30=(0, 1), hand_card_31=(0, 1), hand_card_32=(0, 1),
                          hand_card_33=(0, 1), hand_card_34=(0, 1), hand_card_35=(0, 1), trick_0_card_0=(-1, 35),
                          trick_0_card_1=(-1, 35), trick_0_card_2=(-1, 35), trick_0_card_3=(-1, 35),
                          trick_1_card_0=(-1, 35), trick_1_card_1=(-1, 35), trick_1_card_2=(-1, 35),
                          trick_1_card_3=(-1, 35), trick_2_card_0=(-1, 35), trick_2_card_1=(-1, 35),
                          trick_2_card_2=(-1, 35), trick_2_card_3=(-1, 35), trick_3_card_0=(-1, 35),
                          trick_3_card_1=(-1, 35), trick_3_card_2=(-1, 35), trick_3_card_3=(-1, 35),
                          trick_4_card_0=(-1, 35), trick_4_card_1=(-1, 35), trick_4_card_2=(-1, 35),
                          trick_4_card_3=(-1, 35), trick_5_card_0=(-1, 35), trick_5_card_1=(-1, 35),
                          trick_5_card_2=(-1, 35), trick_5_card_3=(-1, 35), trick_6_card_0=(-1, 35),
                          trick_6_card_1=(-1, 35), trick_6_card_2=(-1, 35), trick_6_card_3=(-1, 35),
                          trick_7_card_0=(-1, 35), trick_7_card_1=(-1, 35), trick_7_card_2=(-1, 35),
                          trick_7_card_3=(-1, 35), trick_8_card_0=(-1, 35), trick_8_card_1=(-1, 35),
                          trick_8_card_2=(-1, 35), trick_8_card_3=(-1, 35), trick_card_0=(-1, 35),
                          trick_card_1=(-1, 35), trick_card_2=(-1, 35), trick_card_3=(-1, 35))
    # Normalize the data
    for feature, feature_range in feature_ranges.items():
        if feature in data_frame:
            data_frame[feature] = (data_frame[feature] - feature_range[0]) / (feature_range[1] - feature_range[0])
    return data_frame
