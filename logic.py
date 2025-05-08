# logic.py — Representation Layer for Connect 4

import copy

def copy_board(board):
    """Returns a deep copy of the board."""
    return copy.deepcopy(board)


def get_valid_moves(board):
    """Returns a list of columns (0-based) where a move can be made."""
    num_cols = len(board[0])
    return [col for col in range(num_cols) if board[0][col] == ' ']


def make_move(board, col, player_symbol):
    """Drops a disc in the specified column and returns (new_board, col)."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_symbol
            break
    return board, col

def is_full(board):
    """Returns True if the board is full (i.e., no empty spaces in the top row)."""
    return all(cell != ' ' for cell in board[0])


def check_winner(board, symbol):
    """Checks if the given symbol has a winning 4-in-a-row on the board."""
    rows, cols = len(board), len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    # Vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Diagonal down-left
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + i][c - i] == symbol for i in range(4)):
                return True

    return False
