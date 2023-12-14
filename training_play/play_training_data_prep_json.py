import os
import numpy as np
import pandas as pd
import json
import glob
from jass.game.game_observation import GameObservation
from jass.game.game_state import GameState

from label_play import LabelPlay


def get_train_data(lines):
    data_array = []
    played_card_array = []
    for line in lines:
        data = json.loads(line)
        state = GameState.from_json(data.get('obs', {}))
        played_card = data.get('action', {})
        played_card_array.append(played_card)
        label_play = LabelPlay.get_label_play(state, played_card)
        data_array.append(label_play.to_dataframe())
    return [data_array, np.array(played_card_array, dtype=np.float32)]
