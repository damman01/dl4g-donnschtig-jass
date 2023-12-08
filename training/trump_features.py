import pandas as pd


def get_features_from_data_frame(data: pd.DataFrame):
    diamonds = data[['DA','DK','DQ','DJ','D10','D9','D8','D7','D6']]
    hearts = data[['HA','HK','HQ','HJ','H10','H9','H8','H7','H6']]
    spades = data[['SA','SK','SQ','SJ','S10','S9','S8','S7','S6']]
    clubs = data[['CA','CK','CQ','CJ','C10','C9','C8','C7','C6']]
    forehand = data[['FH']]

    number_of_diamonds = diamonds.eq(1).sum(axis=1)
    number_of_hearts = hearts.eq(1).sum(axis=1)
    number_of_spades = spades.eq(1).sum(axis=1)
    number_of_clubs = clubs.eq(1).sum(axis=1)

    diamonds_high_cards = diamonds[['DA','DK','DQ','DJ','D10']].eq(1).sum(axis=1)
    hearts_high_cards = hearts[['HA','HK','HQ','HJ','H10']].eq(1).sum(axis=1)
    spades_high_cards = spades[['SA','SK','SQ','SJ','S10']].eq(1).sum(axis=1)
    clubs_high_cards = clubs[['CA','CK','CQ','CJ','C10']].eq(1).sum(axis=1)

    diamonds_low_cards = diamonds[['D9','D8','D7','D6']].eq(1).sum(axis=1)
    hearts_low_cards = hearts[['H9','H8','H7','H6']].eq(1).sum(axis=1)
    spades_low_cards = spades[['S9','S8','S7','S6']].eq(1).sum(axis=1)
    clubs_low_cards = clubs[['C9','C8','C7','C6']].eq(1).sum(axis=1)

    has_diamonds_buur = diamonds[['DJ']]
    has_hearts_buur = hearts[['HJ']]
    has_spades_buur = spades[['SJ']]
    has_clubs_buur = clubs[['CJ']]

    has_diamonds_nell = diamonds[['D9']]
    has_hearts_nell = hearts[['H9']]
    has_spades_nell = spades[['S9']]
    has_clubs_nell = clubs[['C9']]

    x_train_trump = pd.concat([
        number_of_diamonds, number_of_hearts, number_of_spades, number_of_clubs,
        diamonds_high_cards, hearts_high_cards, spades_high_cards, clubs_high_cards,
        diamonds_low_cards, hearts_low_cards, spades_low_cards, clubs_low_cards,
        has_diamonds_buur, has_hearts_buur, has_spades_buur, has_clubs_buur,
        has_diamonds_nell, has_hearts_nell, has_spades_nell, has_clubs_nell,
        forehand
    ], axis=1)

    # Assign column names if needed
    x_train_trump.columns = [
        'number_of_diamonds', 'number_of_hearts', 'number_of_spades', 'number_of_clubs',
        'diamonds_high_cards', 'hearts_high_cards', 'spades_high_cards', 'clubs_high_cards',
        'diamonds_low_cards', 'hearts_low_cards', 'spades_low_cards', 'clubs_low_cards',
        'has_diamonds_buur', 'has_hearts_buur', 'has_spades_buur', 'has_clubs_buur',
        'has_diamonds_nell', 'has_hearts_nell', 'has_spades_nell', 'has_clubs_nell',
        'forehand'
    ]

    return x_train_trump.values


def get_card_columns():
    return [
        # Diamonds
        'DA', 'DK', 'DQ', 'DJ', 'D10', 'D9', 'D8', 'D7', 'D6',
        # Hearts
        'HA', 'HK', 'HQ', 'HJ', 'H10', 'H9', 'H8', 'H7', 'H6',
        # Spades
        'SA', 'SK', 'SQ', 'SJ', 'S10', 'S9', 'S8', 'S7', 'S6',
        # Clubs
        'CA', 'CK', 'CQ', 'CJ', 'C10', 'C9', 'C8', 'C7', 'C6'
    ]


def get_forehand_column():
    return ['FH']
