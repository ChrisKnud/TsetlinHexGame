import math
import random


BOARD_DIM = 11
neighbors = [-(BOARD_DIM+2) + 1, -(BOARD_DIM+2), -1, 1, (BOARD_DIM+2), (BOARD_DIM+2) - 1]

class HexGame:
    def __init__(self):
        self.board = [[0 for _ in range(2)] for _ in range((BOARD_DIM+2)*(BOARD_DIM+2))]
        self.open_positions = [0 for _ in range(BOARD_DIM*BOARD_DIM)]
        self.number_of_open_positions = 0
        self.moves = [0 for _ in range(BOARD_DIM*BOARD_DIM)]
        self.connected = [[0 for _ in range(2)] for _ in range((BOARD_DIM+2)*(BOARD_DIM+2))]
        self.hg_init()

    def hg_init(self):
        for i in range(BOARD_DIM+2):
            for j in range(BOARD_DIM+2):
                self.board[(i*(BOARD_DIM + 2) + j)][0] = 0
                self.board[(i*(BOARD_DIM + 2) + j)][1] = 0

                if 0 < i < BOARD_DIM+1 and 0 < j < BOARD_DIM+1:
                    self.open_positions[(i-1)*BOARD_DIM + j - 1] = i*(BOARD_DIM + 2) + j

                self.connected[(i*(BOARD_DIM + 2) + j)][0] = 1 if i == 0 else 0
                self.connected[(i*(BOARD_DIM + 2) + j)][1] = 1 if j == 0 else 0

        self.number_of_open_positions = BOARD_DIM * BOARD_DIM

    def hg_connect(self, player, position):
        self.connected[position][player] = 1

        if player == 0 and position // (BOARD_DIM + 2) == BOARD_DIM:
            return True

        if player == 1 and position % (BOARD_DIM + 2) == BOARD_DIM:
            return True

        for i in range(6):
            neighbor = position + neighbors[i]
            if self.board[neighbor][player] and not self.connected[neighbor][player]:
                if self.hg_connect(player, neighbor):
                    return True
        return False

    def hg_winner(self, player, position):
        for i in range(6):
            neighbor = position + neighbors[i]
            if self.connected[neighbor][player]:
                return self.hg_connect(player, position)
        return False

    def hg_place_piece_randomly(self, player):
        random_empty_position_index = random.randint(0, self.number_of_open_positions - 1)
        empty_position = self.open_positions[random_empty_position_index]

        self.board[empty_position][player] = 1
        self.moves[BOARD_DIM * BOARD_DIM - self.number_of_open_positions] = empty_position
        self.open_positions[random_empty_position_index] = self.open_positions[self.number_of_open_positions - 1]
        self.number_of_open_positions -= 1

        return empty_position

    def hg_full_board(self):
        return self.number_of_open_positions == 0

    def hg_print(self):
        for i in range(BOARD_DIM):
            print(" " * i, end="")  # Print spaces for board alignment
            for j in range(BOARD_DIM):
                pos = (i+1)*(BOARD_DIM+2) + j + 1
                if self.board[pos][0] == 1:
                    print(" B", end="")
                elif self.board[pos][1] == 1:
                    print(" W", end="")
                else:
                    print(" E", end="")
            print()

    def hg_as_array(self):
        board = []
        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                pos = (i+1)*(BOARD_DIM+2) + j + 1
                if self.board[pos][0] == 1:
                    board.append("B")
                elif self.board[pos][1] == 1:
                    board.append("W")
                else:
                    board.append("E")
        return board



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

def main():
    winner = -1
    data = { 'result': []}
    print("Starting...")
    for game in range(100):
        hg = HexGame()
        player = 0

        print("game: " + str(game))
        while not hg.hg_full_board():
            position = hg.hg_place_piece_randomly(player)
            if hg.hg_winner(player, position):
                winner = player
                break

            player = 1 - player  # Switch players

        if hg.number_of_open_positions >= 75:
            print(f"\nPlayer {winner} wins!\n")
            data["result"].append({'winner': winner, 'board': hg.hg_as_array()})

    for i in range(len(data["result"])):
        print(f'#{i} Winner: {data["result"][i]["winner"]}\n{board_as_string(data["result"][i]["board"])}')

#    with open("./output.json", "w") as file:
   #     json.dump({"winner": winner, "moves": hg.moves}, file)

if __name__ == "__main__":
    main()
