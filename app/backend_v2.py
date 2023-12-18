import json
import os

import jass.game.rule_schieber as rule_schieber
import numpy as np
from jass.game.const import OBE_ABE, UNE_UFE

from jass.game.game_observation import GameObservation
from keras.models import load_model

from training_play.play_training_data_prep_json import get_data_for_play


class Backend:
    """
    The Backend class is responsible for making predictions for the game of Jass.
    It uses trained models to predict the trump and the card to play.
    """

    def __init__(self):
        running_in_docker = os.getenv('RUNNING_IN_DOCKER', 'false') == 'true'
        model_path = '/app/models/' if running_in_docker else '../models/'
        self.trump_model = load_model(model_path + 'trumpModel.keras')
        self.play_model = load_model(model_path + 'playModel.keras')

    def play_card(self, obs: GameObservation) -> int:
        """
        Predicts the card to play based on the game observation.

        Args:
        obs (GameObservation): The game observation.

        Returns:
        int: The index of the card to play.
        """
        prepared_data = self.prepare_play_data(obs)

        valid = rule_schieber.RuleSchieber().get_valid_cards_from_obs(obs)
        predictions = self.play_model.predict(prepared_data)[0]

        # Use the mask to set the invalid predictions to 0
        predictions[~valid.astype(bool)] = 0

        return np.argmax(predictions)

    def select_trump(self, obs: GameObservation) -> int:
        """
        Predicts the trump to select based on the game observation.

        Args:
            obs (GameObservation): The game observation, it must be in a state for trump selection.

        Returns:
            int: Selected trump as encoded in jass.game.const or jass.game.const.PUSH.
        """
        prepared_data = self.prepare_trump_data(obs)
        return np.argmax(self.trump_model.predict(np.array([prepared_data])))

    def prepare_play_data(self, obs: GameObservation) -> np.ndarray:
        """
        Prepares the play data based on the game observation.

        Args:
            obs (GameObservation): The game observation.

        Returns:
            np.ndarray: The prepared play data.
        """
        # add {"obs": to the beginning of the string and "}" to the end of the string
        json_string = '{"obs":' + json.dumps(obs.to_json()) + '}'
        return get_data_for_play(json_string)

    def prepare_trump_data(self, obs: GameObservation) -> np.ndarray:
        """
        Prepares the trump data based on the game observation.

        Args:
            obs (GameObservation): The game observation.

        Returns:
            np.ndarray: The prepared trump data.
        """
        diamonds = obs.hand[0:9]
        hearts = obs.hand[9:17]
        spades = obs.hand[17:26]
        clubs = obs.hand[26:35]
        forehand = [obs.forehand]

        number_of_diamonds = diamonds.sum()
        number_of_hearts = hearts.sum()
        number_of_spades = spades.sum()
        number_of_clubs = clubs.sum()

        diamonds_high_cards = diamonds[:4].sum()
        hearts_high_cards = hearts[:4].sum()
        spades_high_cards = spades[:4].sum()
        clubs_high_cards = clubs[:4].sum()

        diamonds_low_cards = diamonds[4:9].sum()
        hearts_low_cards = hearts[4:9].sum()
        spades_low_cards = spades[4:9].sum()
        clubs_low_cards = clubs[4:9].sum()

        has_diamonds_buur = diamonds[3]
        has_hearts_buur = hearts[3]
        has_spades_buur = spades[3]
        has_clubs_buur = clubs[3]

        has_diamonds_nell = diamonds[5]
        has_hearts_nell = hearts[5]
        has_spades_nell = spades[5]
        has_clubs_nell = clubs[5]

        x_predict_trump = np.hstack((
            number_of_diamonds, number_of_hearts, number_of_spades, number_of_clubs,
            diamonds_high_cards, hearts_high_cards, spades_high_cards, clubs_high_cards,
            diamonds_low_cards, hearts_low_cards, spades_low_cards, clubs_low_cards,
            has_diamonds_buur, has_hearts_buur, has_spades_buur, has_clubs_buur,
            has_diamonds_nell, has_hearts_nell, has_spades_nell, has_clubs_nell,
            forehand
        ))

        return x_predict_trump
