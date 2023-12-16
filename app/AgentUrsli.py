from jass.game.const import card_strings
from jass.game.game_observation import GameObservation
from jass.game.rule_schieber import RuleSchieber
from jass.agents.agent import Agent
from backend_v2 import Backend
import logging

# German strings for trumps
trump_strings = [
    'D: Schellen', 'H: Rosen', 'S: Schilten', 'C: Eichel', 'O: Obe-Abe', 'U: Une-Ufe', '', '', '', '', 'P: Schieben'
]


class AgentUrsli(Agent):
    def __init__(self):
        super().__init__()
        # we need a rule object to determine the valid cards
        self._rule = RuleSchieber()
        self._logger = logging.getLogger(__name__)

    def action_trump(self, obs: GameObservation) -> int:
        """
        Determine trump action for the given observation
        Args:
            obs: the game observation, it must be in a state for trump selection

        Returns:
            selected trump as encoded in jass.game.const or jass.game.const.PUSH
        """
        self._logger.info('Trump request')
        backend = Backend()
        result = backend.select_trump(obs)
        self._logger.log(logging.INFO, "Trump: {}".format(trump_strings[result]))
        return int(result)

    def action_play_card(self, obs: GameObservation) -> int:
        """
        Determine the card to play.

        Args:
            obs: the game observation

        Returns:
            the card to play, int encoded as defined in jass.game.const
        """
        self._logger.info('Card request')
        backend = Backend()
        result = backend.play_card(obs)
        self._logger.log(logging.INFO, "Card: {}".format(card_strings[result]))
        return int(result)
