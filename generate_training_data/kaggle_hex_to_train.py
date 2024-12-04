"""
File used to convert kaggle hex training data to be compatible with my training data
"""
import json
import os.path
import csv
from datetime import datetime


def kaggle_hex_to_train(number_of_items: int = 254, split: bool = True):
    BLACK = '1'
    WHITE = '-1'
    NONE = '0'

    path = os.path.join('D:\\Software_Development\\Artificial_Intellegence\\Datasets\\Hex', "hex_games_1_000_000_size_7.csv")

    dt = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    games = []

    with open(path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            games.append(row)
            count += 1
            if count == number_of_items + 1:
                break

    # Remove csv header from array
    del games[0]

    data = {'result': []}

    # Format hex game
    for game in games:
        for i in range(len(game)):
            if game[i] == BLACK:
                game[i] = 'B'
            if game[i] == WHITE:
                game[i] = 'W'
            if game[i] == NONE:
                game[i] = 'E'

        data['result'].append({
            'winner': game[len(game)-1],
            'board': game[:len(game)-1],
        })

    if split:
        split_pos = int(len(data['result'])/2)

        train_data = {'result': data['result'][:split_pos]}
        test_data = {'result': data['result'][split_pos:]}

        with open(f"../data/kaggle/train-kaggle-{dt}.json", "w") as f:
            f.write(json.dumps(train_data, indent=4))

        with open(f"../data/kaggle/eval-kaggle-{dt}.json", "w") as f:
            f.write(json.dumps(test_data, indent=4))
    else:
        with open(f"../data/kaggle/train-kaggle-{dt}.json", "w") as f:
            f.write(json.dumps(data, indent=4))


kaggle_hex_to_train(number_of_items=508, split=True)