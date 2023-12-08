import unittest

from jass.game.const import *
from jass.game.game_observation import GameObservation
from app.backend import Backend

class TestSelectTrump(unittest.TestCase):
    def test_select_trump(self):
        obs = GameObservation()
        obs.hand = np.array([1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        obs.forehand = 0
        backend = Backend()
        trump = backend.select_trump(obs)
        print(trump)
        self.assertIn(trump, range(5))
        self.assertNotEqual(trump, PUSH)
        self.assertEqual(trump, HEARTS)
