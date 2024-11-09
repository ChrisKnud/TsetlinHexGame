"""
File used to convert kaggle hex training data to be compatible with my training data
"""
import argparse
import json
import math
import os.path
import csv
from datetime import datetime
from os.path import split


def kaggle_hex_to_train(number_of_items: int = 1000, split: bool = True):
    BLACK = '1'
    WHITE = '-1'
    NONE = '0'

    # Download latest version
    path = os.path.join('D:\\Software_Development\\Artificial_Intellegence\\Datasets\\Hex', "hex_games_1_000_000_size_7.csv")

    dt = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    games = []

    with open(path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            games.append(row)
            count += 1
            if count == number_of_items:
                break

    # Remove csv header from array
    del games[0]

    data = []

    # Format hex game
    for game in games:
        for i in range(len(game)):
            if game[i] == BLACK:
                game[i] = 'B'
            if game[i] == WHITE:
                game[i] = 'W'
            if game[i] == NONE:
                game[i] = 'E'

        data.append({
            'winner': game[len(game)-1],
            'board': game[:len(game)-1],
        })

    if split:
        with open(f"../data/kaggle/train-kaggle-{dt}.json", "w") as f:
            f.write(json.dumps(data[:int(len(data)/2)], indent=4))

        with open(f"../data/kaggle/eval-kaggle-{dt}.json", "w") as f:
            f.write(json.dumps(data[int(len(data)/2):], indent=4))
    else:
        with open(f"../data/kaggle/train-kaggle-{dt}.json", "w") as f:
            f.write(json.dumps(data, indent=4))