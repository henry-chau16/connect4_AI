from logic import get_valid_moves, make_move, is_full, check_winner, copy_board
import inference
import random

### ----------------------------------- SEARCH ------------------------------------------- ###
### -------------------------------------------------------------------------------------- ###

# Evaluate the current board using the inference engine
# Converts the board into logical facts and returns a score based on predefined rules
def evaluate_board(board, target):
    inference.reset_facts()                  # Clear any existing facts in the inference engine
    inference.board_to_facts(board, target)         # Add current board state as facts
    return inference.get_board_score()      # Get a rule-based score for the current board

# Minimax algorithm with alpha-beta pruning
# Recursively simulates game states to determine the best move

def minimax(board, depth, is_maximizing, alpha, beta, my_symbol, opponent_symbol):
    # Check for terminal conditions: win, lose, or draw, or depth limit
    if check_winner(board, my_symbol):
        return 1000                          # Winning board state for the current player
    elif check_winner(board, opponent_symbol):
        return -1000                         # Losing board state for the current player
    elif is_full(board) or depth == 0:
        return evaluate_board(board, my_symbol)        # Evaluate non-terminal state if depth limit reached

    if is_maximizing:
        max_eval = float('-inf')            # Initialize maximum evaluation score
        for col in get_valid_moves(board):  # Loop through each valid move
            new_board, _ = make_move(copy_board(board), col, my_symbol)  # Simulate move
            eval_score = minimax(new_board, depth - 1, False, alpha, beta, my_symbol, opponent_symbol)  # Recurse as minimizing player
            max_eval = max(max_eval, eval_score)   # Track max score
            alpha = max(alpha, eval_score)         # Update alpha
            if beta <= alpha:
                break                       # Prune the branch
        return max_eval
    else:
        min_eval = float('inf')             # Initialize minimum evaluation score
        for col in get_valid_moves(board):
            new_board, _ = make_move(copy_board(board), col, opponent_symbol)  # Simulate opponent's move
            eval_score = minimax(new_board, depth - 1, True, alpha, beta, my_symbol, opponent_symbol)  # Recurse as maximizing player
            min_eval = min(min_eval, eval_score)   # Track min score
            beta = min(beta, eval_score)           # Update beta
            if beta <= alpha:
                break                       # Prune the branch
        return min_eval

# Chooses the best move for the current player using minimax evaluation
def choose_best_move(board, my_symbol, depth):
    opponent_symbol = 'O' if my_symbol == 'X' else 'X'  # Determine opponent's symbol
    best_score = float('-inf')            # Initialize best score
    best_col = None                       # Initialize best move (column)

    for col in get_valid_moves(board):
        new_board, _ = make_move(copy_board(board), col, my_symbol)
        score = minimax(new_board, depth - 1, False, float('-inf'), float('inf'), my_symbol, opponent_symbol)
        if score > best_score:
            best_score = score
            best_cols = [col]  # New best score, start fresh
        elif score == best_score:
            best_cols.append(col)  # Same best score, add to options

    return random.choice(best_cols)  # Randomly choose among best                   # Return the column with the best evaluation