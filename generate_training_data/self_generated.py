import json
import math
import os
import random
from datetime import datetime

#from format import board_as_string
from generate_training_data.util.check_winner import check_winner


class HexBoard:

    # Symbols [Player 1, Player 2, Empty Cell]
    def __init__(self, size, symbols):
        self.size = size
        self.symbols = symbols
        self.board = [self.symbols[2] for _ in range(self.size ** 2)]
        self.winner = None
        self.count = 0 # Current turn


    def make_board(self):
        return self._populate()


    def board_as_json(self):
        return {
            "winner": self.winner,
            "board": self.board,
        }


    """
    Remove a certain number of players from the board.
    This returns an unfinished board but with a known winner.
    """
    def remove_players(self, count):
        if self.winner is None:
            raise ValueError("Board has no winner. Please generate a full board first.")

        player = random.randint(0, 1)

        for i in range(count):
            index = random.randint(0, len(self.board) - 1)

            # Make sure the removed piece is not empty
            if player == 0:
                # Make sure the piece to remove is symbol 2
                while self.board[index] != self.symbols[0]:
                    index = random.randint(0, len(self.board) - 1)

                self.board[index] = self.symbols[2]
                #print(f"player {player} on index {index} set to {self.symbols[2]}")
                player = 1
                continue


            if player == 1:
                # Make sure the piece to remove is symbol 1
                while self.board[index] != self.symbols[1]:
                    index = random.randint(0, len(self.board) - 1)

                self.board[index] = self.symbols[2]
                #print(f"player {player} on index {index} set to {self.symbols[2]}")
                player = 0
                continue


    def _populate(self):
        available_positions = list(range(len(self.board)))
        finished = False

        player = random.randint(0, 1)
        is_player_1 = player == 0

        while not finished:
            if not available_positions:
                print("No winner, clearing board.")
                self.board.clear()
                available_positions = self._reset_board()

            index = random.choice(available_positions)
            available_positions.remove(index)

            if is_player_1:
                self.board[index] = self.symbols[0]
            else:
                self.board[index] = self.symbols[1]

            self.count += 1

            winner = check_winner(self.board, self.size)
            if winner is not None:
                self.winner = winner
                finished = True
            else:
                is_player_1 = not is_player_1

    def _reset_board(self):
        self.board = [self.symbols[2] for _ in range(self.size ** 2)]
        return list(range(len(self.board)))

def board_as_string(board):
    board_width = int(math.sqrt(len(board)))

    board_str = ""
    for i in range(len(board)):
        if board[i] == 'E':
            board_str += '. '
        else:
            board_str += str(board[i]) + " "
        if i != 0 and i % board_width == board_width - 1:
            board_str += "\n"

    return board_str


# Moves left: Number of moves before the game is finished
# randomize: Randomize number of missing pieces. Max count of pieces to remove
def generate_hex_games(size, count, moves_left=0, split=False, randomize=0):
    boards = []
    for i in range(count):
        hexboard = HexBoard(size, ["B", "W", "E"])
        hexboard.make_board()

        if moves_left > 0 and randomize == 0:
            hexboard.remove_players(moves_left)
        elif randomize > 0:
            hexboard.remove_players(random.randint(0, randomize))

        boards.append(hexboard.board_as_json())
        print(i)
    dt = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    board_width = int(math.sqrt(len(boards[0]["board"])))

    path = os.path.join("data", "self")

    if split:
        split_pos = int(len(boards)/2)

        train_data = {'result': boards[:split_pos]}
        test_data = {'result': boards[split_pos:]}

        with open(os.path.join(path, f"train-self-{board_width}-{int(len(boards)/2)}-{moves_left}-{randomize}-{dt}.json"), "w") as f:
            f.write(json.dumps(train_data, indent=4))

        with open(os.path.join(path, f"eval-self-{board_width}-{int(len(boards)/2)}-{moves_left}-{randomize}-{dt}.json"), "w") as f:
            f.write(json.dumps(test_data, indent=4))
    else:
        with open(os.path.join(path, f"train-self-{board_width}-{int(len(boards))}-{moves_left}-{randomize}-{dt}.json"), "w") as f:
            f.write(json.dumps({"result": boards}, indent=4))


generate_hex_games(3, 5, moves_left=0, split=False, randomize=0)