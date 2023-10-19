from jass.game.game_util import *
from jass.game.const import *
from jass.game.game_observation import GameObservation

from config import *


def select_trump(obs: GameObservation):
    """
    Determine trump action for the given observation.

    Args:
        obs (GameObservation): The game observation, it must be in a state for trump selection.

    Returns:
        int: Selected trump as encoded in jass.game.const or jass.game.const.PUSH.
    """
    cards = obs.hand
    have_puur_with_four(cards)

    hand_list = convert_one_hot_encoded_cards_to_int_encoded_list(obs.hand)
    scores = [calculate_trump_selection_score(hand_list, trump) for trump in range(6)]
    high_score = np.argmax(scores)

    # if forehand is not yet set, we are the forehand player and can select trump or push
    if obs.forehand == -1:
        if scores[high_score] > TRUMP_THRESHOLD:
            return high_score
        else:
            return PUSH
    return high_score


def have_puur_with_four(hand: np.ndarray) -> np.ndarray:
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


def calculate_trump_selection_score(cards, trump: int) -> int:
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
