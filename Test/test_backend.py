import unittest

import numpy as np
from jass.game.const import *
from jass.game.game_observation import GameObservation
from backend import select_trump

class TestSelectTrump(unittest.TestCase):
    def test_select_trump(self):
        obs = GameObservation()
        obs.hand = np.array([1, 1, 0 ,0 ,0 ,1 ,0 ,0 ,1 ,1 ,0 ,1 ,1 ,0 ,0 ,1 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0])
        trump = select_trump(obs)
        self.assertIn(trump, range(5))
        self.assertNotEqual(trump, PUSH)
        self.assertEqual(trump, HEARTS)
