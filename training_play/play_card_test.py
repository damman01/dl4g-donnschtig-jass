import json
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from jass.game.const import card_strings
from jass.game.game_observation import GameObservation

from app.backend_v2 import Backend


class TestBackend(unittest.TestCase):

    def test_valid_card_is_played(self):
        # Arrange
        data = json.load(open('test_files/single/jass_single.txt'))

        backend = Backend()
        obs = GameObservation()
        obs = (obs.from_json(data['obs']))

        # Act
        result = backend.play_card(obs)
        print("Valid Cards:", card_strings[4], card_strings[8], card_strings[34])
        print("Result:", card_strings[result])

        # Assert that the result is a valid card 4, 8, 34
        self.assertIn(result, [4, 8, 34])
