import random

import jass.game.rule_schieber
from jass.game.game_util import *
from jass.game.const import *
from jass.game.game_observation import GameObservation
from keras.models import load_model


class Backend:

    def play_card(self, obs: GameObservation):
        schieber = jass.game.rule_schieber.RuleSchieber()
        valid = jass.game.rule_schieber.RuleSchieber.get_valid_cards_from_obs(schieber, obs)
        array = convert_one_hot_encoded_cards_to_str_encoded_list(valid)
        rdm = random.choice(array)
        card_id = card_ids[rdm]
        return card_id

    def select_trump(self, obs: GameObservation):
        """
        Determine trump action for the given observation.

        Args:
            obs (GameObservation): The game observation, it must be in a state for trump selection.

        Returns:
            int: Selected trump as encoded in jass.game.const or jass.game.const.PUSH.
        """
        prepared_data = self.prepare_data(obs)
        return self.make_prediction(prepared_data)

    def prepare_data(self, obs: GameObservation) -> np.ndarray:
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

        x_train_trump = np.hstack((
            number_of_diamonds, number_of_hearts, number_of_spades, number_of_clubs,
            diamonds_high_cards, hearts_high_cards, spades_high_cards, clubs_high_cards,
            diamonds_low_cards, hearts_low_cards, spades_low_cards, clubs_low_cards,
            has_diamonds_buur, has_hearts_buur, has_spades_buur, has_clubs_buur,
            has_diamonds_nell, has_hearts_nell, has_spades_nell, has_clubs_nell,
            forehand
        ))

        return x_train_trump
        
    def make_prediction(self, prepared_data: np.ndarray) -> int:
        model = load_model('../models/trumpModel.keras')
        predictions = model.predict(np.array([prepared_data]))
        return np.argmax(predictions)

    def have_puur_with_four(self, hand: np.ndarray) -> np.ndarray:
        result = np.zeros(4, dtype=int)

        for color in range(4):
            # Check if the player has the Jack of the current color.
            if hand[color * 9 + 3] == 1:
                # Count the number of cards of the current color.
                num_cards = np.sum(hand[color * 9:color * 9 + 8])
                # If the player has 4 or more cards of the current color, the rule is fulfilled.
                if num_cards >= 4:
                    result[color] = 1
        return result

    def calculate_trump_selection_score(self, cards, trump: int) -> int:
        """Calculates the score of a hand for selecting trump.

        Args:
            cards: A list of 9 cards, encoded as integers.
            trump: The trump suit.

        Returns:
            The score of the hand for selecting trump.
        """
        # Score for each card of a color from Ace to 6

        # score if the color is trump
        trump_score = [15, 10, 7, 25, 6, 19, 5, 5, 5]
        # score if the color is not trump
        no_trump_score = [9, 7, 5, 2, 1, 0, 0, 0, 0]
        # score if obenabe is selected (all colors)
        obenabe_score = [14, 10, 8, 7, 5, 0, 5, 0, 0, ]
        # score if uneufe is selected (all colors)
        uneufe_score = [0, 2, 1, 1, 5, 5, 7, 9, 11]

        score = 0
        for card in cards:
            color = card // 9
            offset = card - (color * 9)

            # If the color is trump, use the trump score.
            if color == trump:
                score += trump_score[offset]
            # If obenabe is selected, use the obenabe score.
            elif trump == OBE_ABE:
                score += obenabe_score[offset]
            # If uneufe is selected, use the uneufe score.
            elif trump == UNE_UFE:
                score += uneufe_score[offset]
            # If the color is not trump and obenabe is not selected, use the no-trump score.
            elif color != trump:
                score += no_trump_score[offset]

        return score
