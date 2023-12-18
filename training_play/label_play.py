# label_play.py
import logging

import numpy as np
import pandas as pd
from dataclasses import dataclass, field

from jass.game.const import team, next_player, same_team, card_values
from jass.game.game_state import GameState
from jass.game.game_util import get_cards_encoded_from_str
from jass.game.rule_schieber import RuleSchieber


class LabelPlay:
    """
    Class to define (possible) training information for a specific action in the game when it is in the playing
    stage (i.e. not in the trump defining stage).

    This includes the card played, the points made in the current trick by the own team and the other, the player who
    won the trick, the points made in the game by the own team and the other and the hands the players had at the
    beginning of the game.

    (Adding both the points for own and opposite team for the points in the trick eliminates needing to know the
    current player. Adding the information about the exact winner (instead of the team) might help to forecast the
    result of the trick)

    """

    @dataclass
    class LabelPlay:
        points_in_trick_own: int
        points_in_trick_other: int
        trick_winner: int
        points_in_game_own: int
        points_in_game_other: int
        declared_trump: int
        trump: int
        forehand: int
        nr_tricks: int
        nr_cards_in_trick: int
        hand: np.ndarray = field(default_factory=list)
        tricks: np.ndarray = field(default_factory=list)

    def __init__(self,
                 points_in_trick_own: int,
                 points_in_trick_other: int,
                 trick_winner: int,
                 points_in_game_own: int,
                 points_in_game_other: int,
                 declared_trump: int,
                 trump: int,
                 forehand: int,
                 nr_tricks: int,
                 nr_cards_in_trick: int,
                 hand: np.ndarray,
                 tricks: np.ndarray):
        self.points_in_trick_own = points_in_trick_own
        self.points_in_trick_other = points_in_trick_other
        self.trick_winner = trick_winner
        self.points_in_game_own = points_in_game_own
        self.points_in_game_other = points_in_game_other
        self.declared_trump = declared_trump
        self.trump = trump
        self.forehand = forehand
        self.nr_tricks = nr_tricks
        self.nr_cards_in_trick = nr_cards_in_trick
        self.hand = hand
        self.tricks = tricks


    @classmethod
    def get_label_play(cls, game: GameState, card_nr: int) -> 'LabelPlay':
        """
        Generate a label play from the data. The player and hands arguments could be calculated from the game,
        however as is it expensive to calculate, it has to be submitted as an argument, so it could be used for
        several card plays from the same game.

        Args:
            game: completed game
            card_nr: which card was played in the game (0..35)
        Returns:
            a LabelPlay with this information
        """
        nr_trick = game.nr_tricks
        player = game.player

        hand = game.hands[player]
        tricks = game.tricks

        team_own = team[player]
        team_other = team[next_player[player]]

        rule = RuleSchieber()

        points_in_trick = rule.calc_points(game.current_trick, nr_trick == 8, game.trump)
        trick_winner = rule.calc_winner(game.current_trick, game.trick_first_player, game.trump)[nr_trick]

        if same_team[player, trick_winner]:
            points_in_trick_own = points_in_trick
            points_in_trick_other = 0
        else:
            points_in_trick_own = 0
            points_in_trick_other = points_in_trick

        label_play = LabelPlay(points_in_game_own=game.points[team_own],
                               points_in_game_other=game.points[team_other],
                               trick_winner=trick_winner,
                               points_in_trick_own=points_in_trick_own,
                               points_in_trick_other=points_in_trick_other,
                               declared_trump=game.declared_trump,
                               trump=game.trump,
                               forehand=game.forehand,
                               nr_tricks=game.nr_tricks,
                               nr_cards_in_trick=game.nr_cards_in_trick,
                               hand=hand,
                               tricks=tricks)
        return label_play

    def to_json(self) -> dict:
        """
        Convert to json
        Returns:
            dict that can be serialized to json
        """
        return dict(
            points_in_trick_own=int(self.points_in_trick_own),
            points_in_trick_other=int(self.points_in_trick_other),
            trick_winner=int(self.trick_winner),
            points_in_game_own=int(self.points_in_game_own),
            points_in_game_other=int(self.points_in_game_other),
            declared_trump=int(self.declared_trump),
            trump=int(self.trump),
            forehand=int(self.forehand),
            nr_tricks=int(self.nr_tricks),
            nr_cards_in_trick=int(self.nr_cards_in_trick),
            hand_player=self.hand,
            tricks=self.tricks
        )

    @classmethod
    def from_json(cls, data):
        """
        Create label from dict (from json)
        Args:
            data: dict representation
        Returns:
            label from the data
        """
        hand = np.zeros(shape=[1, 36], dtype=np.int32)
        try:
            hand = get_cards_encoded_from_str(data['hand_player'])

        except KeyError as e:
            logging.getLogger(__name__).error('Key error: {}, data: {}'.format(e, data))
            raise e

        return LabelPlay(points_in_trick_own=data['points_in_trick_own'],
                         points_in_trick_other=data['points_in_trick_other'],
                         trick_winner=data['trick_winner'],
                         points_in_game_own=data['points_in_game_own'],
                         points_in_game_other=data['points_in_game_other'],
                         declared_trump=data['declared_trump'],
                         trump=data['trump'],
                         forehand=data['forehand'],
                         nr_tricks=data['nr_tricks'],
                         nr_cards_in_trick=data['nr_cards_in_trick'],
                         hand=hand,
                         tricks=data['tricks'])

    def to_dataframe(self):
        """
        Converts the LabelPlay object to a pandas DataFrame.
        Returns:
            DataFrame: The LabelPlay object in DataFrame format.
        """
        # Convert the hands array to a DataFrame
        hand_df = pd.DataFrame(self.hand.flatten().reshape(1, -1),
                                columns=[f'hand_card_{i % 36}' for i in range(self.hand.size)])

        # tricks_df = pd.DataFrame(self.tricks.flatten().reshape(1, -1),
        #                         columns=[f'trick_{i // 4}_card_{i % 4}' for i in range(self.tricks.size)])
        tricks_df = pd.DataFrame(self.tricks[self.nr_tricks].flatten().reshape(1, -1),
                                columns=[f'trick_card_{i % 4}' for i in range(self.tricks[self.nr_tricks].size)])

        # Convert the other attributes to a DataFrame
        df = pd.DataFrame(
            data={
                "points_in_trick_own": [self.points_in_trick_own],
                "points_in_trick_other": [self.points_in_trick_other],
                "trick_winner": [self.trick_winner],
                # "points_in_game_own": [self.points_in_game_own],
                # "points_in_game_other": [self.points_in_game_other],
                # "declared_trump": [self.declared_trump],
                "trump": [self.trump],
                # "forehand": [self.forehand],
                "nr_tricks": [self.nr_tricks],
                "nr_cards_in_trick": [self.nr_cards_in_trick]
            }
        )

        # Concatenate the two DataFrames along the columns axis
        df = pd.concat([df, hand_df, tricks_df], axis=1)

        return df
