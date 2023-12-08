import logging

import numpy as np

from jass.game.const import team, next_player, same_team
from jass.game.game_state import GameState
from jass.game.game_util import convert_one_hot_encoded_cards_to_str_encoded_list, get_cards_encoded_from_str
from jass.train.label_play 