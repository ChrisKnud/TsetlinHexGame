from datetime import datetime
import json
from format import train_data_from_file

"""
Run this to produce a json file containing training data
produced by the C code provided by granmo.

First use regex to edit data to be on the following format:
Player 0 wins!
E E E E E B W E W E W
E E W B E B B E E W B
W E E E E B E B W W E
E E E E B B W E E E E
E W E E E B B B E E E
E W E W E E E B B E W
E E W E E W E E B E E
W E E E B E W E B E E
E W E W E E B W B E E
B W E E E E E E B W E
E E E E E E B B E E E
[NEW GAME]
Player 1 wins!
E B E E E E W B E E E
E E E E B E E B E E E
B E B E B E E W B E E
E E E W E E E E E E E
E B E E E E B E E E E
B B W E E E B W W W W
E E E E E E W B E B E
E B E E E W E B B E E
E B E B W E W E E W E
W E E W W E B E E W W
W W W W E E B W B E E
[NEW GAME]
"""

file_name = 'hex_train'

with open(f"data/{file_name}.txt", "r") as f:
    lines = f.readlines()

    games = {'result' : []}

    winner = ""
    board = []
    for line in lines:
        if line.startswith("Player "):
            winner = 'B' if line[7] == '0' else 'W'
            continue
        for letter in line:
            if letter == 'B' or letter == 'W' or letter == 'E':
                board.append(letter)

        if line.startswith("[!?!?!?]"):
            games['result'].append({
                'winner': winner,
                'board': board
            })
            winner = ""
            board = []


with open(f"data/{file_name}.json", "w") as f:
    f.write(json.dumps(games, indent=4))



data = train_data_from_file(f"data/{file_name}.json")



dt = datetime.now()
ts = datetime.timestamp(dt)
print(dt)