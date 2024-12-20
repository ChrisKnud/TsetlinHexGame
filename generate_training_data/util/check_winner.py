"""
Helper function generated by chatGPT to determined if a player has won.
This is used to stop placing any more pieces when generating a hex board.
Ensuring not all boards to be full
"""

def check_winner(board, size):
    """
    Checks for the winner of a Hex game represented as a 1D array.

    Args:
        board (list of str): The Hex game board as a 1D list where:
            - 'B' represents Black pieces,
            - 'W' represents White pieces,
            - 'E' represents empty cells.
        size (int): The width/height of the Hex board (assumed square).

    Returns:
        str: 'B' if Black wins, 'W' if White wins, or None if there is no winner.
    """
    visited = set()

    winner = []
    def dfs(index, player, goal_check):
        if goal_check(index):
            return True
        visited.add(index)
        for neighbor in get_neighbors(index):
            if neighbor not in visited and board[neighbor] == player:
                if dfs(neighbor, player, goal_check):
                    return True
        return False

    def get_neighbors(index):
        """Get valid neighbors for the given index in the 1D array."""
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)  # Hexagonal directions
        ]
        neighbors = []
        x, y = index // size, index % size  # Convert 1D index to 2D coordinates
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size:  # Ensure within bounds
                neighbors.append(nx * size + ny)  # Convert back to 1D index
        return neighbors

    # Check for Black ('B') (Left to Right)
    for x in range(size):
        if board[x * size] == 'B':  # Start on left edge
            if dfs(x * size, 'B', lambda idx: idx % size == size - 1):  # Goal is reaching right edge
                winner.append('B')

    # Check for White ('W') (Top to Bottom)
    for y in range(size):
        if board[y] == 'W':  # Start on top edge
            if dfs(y, 'W', lambda idx: idx // size == size - 1):  # Goal is reaching bottom edge
                winner.append('W')

    # Return a winner only if there is one
    if len(winner) == 1:
        return winner[0]
    else:
        return None

