import pandas as pd
from pathlib import Path
from training.trump_features import get_features_from_data_frame, get_card_columns, get_forehand_column


def get_train_data():
    path_to_data = Path('../data/2018_10_18_trump_without_header.csv')
    path_to_player_ids = Path('../data/top_third_players.csv')

    # Import only a fraction of data for efficient testing
    data = pd.read_csv(path_to_data, header=None)
    # Import the ids of the best third of players in the dataset.
    top_player_ids = pd.read_csv(path_to_player_ids, header=None)

    user = ['user']
    trump = ['trump']

    data.columns = get_card_columns() + get_forehand_column() + user + trump

    filtered_data = data[data['user'].isin(top_player_ids[0])]

    numpy_x_train_trump = get_features_from_data_frame(filtered_data)
    numpy_y_train_trump = filtered_data[trump].values
    return [numpy_x_train_trump, numpy_y_train_trump]
