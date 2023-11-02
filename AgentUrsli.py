from jass.game.game_observation import GameObservation
from jass.game.rule_schieber import RuleSchieber
from jass.agents.agent import Agent

from backend import Backend

class AgentUrsli(Agent):
    def __init__(self):
        super().__init__()
        # we need a rule object to determine the valid cards
        self._rule = RuleSchieber()

    def action_trump(self, obs: GameObservation) -> int:
        """
        Determine trump action for the given observation
        Args:
            obs: the game observation, it must be in a state for trump selection

        Returns:
            selected trump as encoded in jass.game.const or jass.game.const.PUSH
        """
        backend = Backend()
        return backend.select_trump(obs)

    def action_play_card(self, obs: GameObservation) -> int:
        """
        Determine the card to play.

        Args:
            obs: the game observation

        Returns:
            the card to play, int encoded as defined in jass.game.const
        """
        backend = Backend()
        return backend.play_card(obs)

