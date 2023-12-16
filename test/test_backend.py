import unittest

from jass.game.const import *
from jass.game.game_observation import GameObservation
from app.backend_v2 import Backend as Backend_V2
from app.backend_v1 import Backend as Backend_V1

class TestSelectTrump(unittest.TestCase):
    def test_select_trump(self):
        obs = GameObservation()
        obs.hand = np.array([1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0])
        obs.forehand = -1
        backend_v1 = Backend_V1()
        backend_v2 = Backend_V2()
        trump_v1 = backend_v1.select_trump(obs)
        trump_v2 = backend_v2.select_trump(obs)
        print(trump_v1)
        print(trump_v2)
        self.assertEqual(trump_v1, trump_v2)
