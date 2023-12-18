import os

import numpy as np
from jass.game.const import card_strings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from pathlib import Path

from keras.models import load_model
import json
from training_play.play_training import data_generator
import logging

script_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

paths_to_data = os.path.join(script_dir, "./test_files/small/")
print('Searching directory...:', paths_to_data)
test_files = []

for file in Path(paths_to_data).rglob('*.txt'):
    test_files.append(file)
test_files.sort()
print('Found {} files.'.format(len(test_files)))

# Generate the test data
test_gen = data_generator(test_files)

# Load the model
model = load_model('../models/playModel.keras')

# get the predictions
predictions = model.predict(test_gen, steps=len(test_files))
# Print out the predictions
print(f"Predictions: {predictions}")
# get the index of the highest probability
predictions = np.argmax(predictions, axis=1)


# get every action from the test data, every line in the test data contains a json with a "action":card_id
actions = []
for file in test_files:
    with open(file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data = json.loads(line)
            actions.append(data["action"])

# compare them to the predictions
correct = 0
for action, prediction in zip(actions, predictions):
    if action == prediction:
        correct += 1

# get the card strings from the predictions
card_predictions = [card_strings[prediction] for prediction in predictions]

# get the card strings from the actions
card_actions = [card_strings[action] for action in actions]


print(f"Predictions: {card_predictions}")
print(f"Actions    : {card_actions}")
print(f"Correct predictions: {correct}")
