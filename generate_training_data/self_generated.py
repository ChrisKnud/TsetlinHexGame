import json
import random
from datetime import datetime

from generate_training_data.util.check_winner import check_winner


class HexBoard:

    # Symbols [Player 1, Player 2, Empty Cell]
    def __init__(self, size, symbols):
        self.size = size
        self.symbols = symbols
        self.board = [symbols[2] for _ in range(size**2)]
        self.winner = None
        self.count = 0 # Current turn


    def board_as_str(self):
        print("Board len: " + str(len(self.board)))
        board_str = f"Winner: {self.winner}\n"
        for i in range(len(self.board)):
            if i % self.size == 0 and i != 0:
                board_str += "\n"

            board_str += f"{str(self.board[i])} "

        return board_str

    def make_board(self):
        return self._populate()


    def board_as_json(self):
        return {
            "winner": self.winner,
            "board": self.board,
        }

    def _populate(self):
        print("board: " + str(self.board))
        for i in range(len(self.board)):
            index = random.randint(0, len(self.board) - 1)

            while self.board[index - 1] != self.symbols[2]:
                index = random.randint(0, len(self.board) - 1)
                print("Index " + str(index))

            if self.count % 2 == 0:
                self.board[index-1] = self.symbols[0]
            else:
                self.board[index - 1] = self.symbols[1]

            self.count += 1

            winner = check_winner(self.board, self.size)

            if check_winner(self.board, self.size) is not None:
                self.winner = winner
                return

        print("board " + str(self.board))


def generate_hex_games(size, count, split=False):
    hexboard = HexBoard(size, ["B", "W", "."])

    boards = []
    for i in range(count):
        hexboard.make_board()
        print(hexboard.board_as_str())
        print(hexboard.board_as_json())
        boards.append(hexboard.board_as_json())

    dt = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    path = f"D:\\Software_Development\\Artificial_Intellegence\\TsetlingMachine\\TsetlinHexGame\\data\\self"

    if split:
        split_pos = int(len(boards)/2)

        train_data = {'result': boards[:split_pos]}
        test_data = {'result': boards[split_pos:]}

        with open(f"{path}\\train-self-{dt}.json", "w") as f:
            f.write(json.dumps(train_data, indent=4))

        with open(f"{path}\\eval-self-{dt}.json", "w") as f:
            f.write(json.dumps(test_data, indent=4))
    else:
        with open(f"{path}\\train-self-{dt}.json", "w") as f:
            f.write(json.dumps({"result": boards}, indent=4))


generate_hex_games(7, 8, True)