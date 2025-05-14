# inference.py — Durable Rules Based Inference Engine for Connect 4

import logging

# Setup logging for rules fired
logging.basicConfig(
    filename='inference_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)


### -------------------------------- REPRESENTATION & REASONING ---------------------------------- ###
### ------------- (The representation and reasoning layers are mostly integrated) -----------------###

from durable.lang import *

# === RULE BASE ======================================================================== #

global_score = {'value': 0}

with ruleset('connect4'):

    ### OFFENSIVE (SCORING) RULES ### --------------------------------------------------

    @when_all(
        m.type == 'board'
    )
    def analyze_board(c):
        board = c.m.board
        target = c.m.target
        rows = len(board)
        cols = len(board[0])
        center_col = cols // 2
        opponent = 'O' if target == 'X' else 'X'

        ### WIN 4 in a row

        # Horizontal
        for r in range(rows):
            for c0 in range(cols - 3):
                if (board[r][c0] == target and
                    board[r][c0+1] == target and
                    board[r][c0+2] == target and
                    board[r][c0+3] == target):
                    logger.info(f"[RULE FIRED] Detected horizontal win at row {r}, col {c0}")
                    global_score['value'] += 1000
                    logger.info(f"score {global_score['value']}")
        
        # Vertical
        for r in range(rows - 3):
            for c0 in range(cols):
                if (board[r][c0] == target and
                    board[r + 1][c0] == target and
                    board[r + 2][c0] == target and
                    board[r + 3][c0] == target):
                    logger.info(f"[Vertical Win] at col {c0}, starting row {r}")
                    global_score['value'] += 1000
                    logger.info(f"score {global_score['value']}")

        # Diag down left
        for r in range(rows - 3):
            for c0 in range(cols - 3):
                if (board[r][c0] == target and
                    board[r + 1][c0 + 1] == target and
                    board[r + 2][c0 + 2] == target and
                    board[r + 3][c0 + 3] == target):
                    logger.info(f"[Positive Diagonal Win] from ({r},{c0})")
                    global_score['value'] += 1000
                    logger.info(f"score {global_score['value']}")
        
        # Diag down right
        for r in range(3, rows):
            for c0 in range(cols - 3):
                if (board[r][c0] == target and
                    board[r - 1][c0 + 1] == target and
                    board[r - 2][c0 + 2] == target and
                    board[r - 3][c0 + 3] == target):
                    logger.info(f"[Negative Diagonal Win] from ({r},{c0})")
                    global_score['value'] += 1000 
                    logger.info(f"score {global_score['value']}")

        ### Open Triple

        # Horizontal
        for r in range(rows):
            for c0 in range(cols - 3):
                window = [board[r][c0 + i] for i in range(4)]
                if (window[:3] == [target] * 3 and window[3] == ' ') or \
                (window[0] == ' ' and window[1:] == [target] * 3):
                    logger.info(f"[Open Horizontal Triple] at row {r}, col {c0}")
                    global_score['value'] += 50
                    logger.info(f"score {global_score['value']}")

        # Vertical
        for r in range(rows - 3):
            for c0 in range(cols):
                if (board[r][c0] == target and
                    board[r + 1][c0] == target and
                    board[r + 2][c0] == target and
                    board[r + 3][c0] == ' '):
                    logger.info(f"[Open Vertical Triple] at col {c0}, starting row {r}")
                    global_score['value'] += 50
                    logger.info(f"score {global_score['value']}")

        # Diag down left
        for r in range(rows - 3):
            for c0 in range(cols - 3):
                diag = [board[r + i][c0 + i] for i in range(4)]
                if diag[:3] == [target] * 3 and diag[3] == ' ':
                    logger.info(f"[Open ↘ Triple] from ({r},{c0})")
                    global_score['value'] += 50
                    logger.info(f"score {global_score['value']}")
                elif diag[0] == ' ' and diag[1:] == [target] * 3:
                    logger.info(f"[Open ↘ Triple] ending at ({r+3},{c0+3})")
                    global_score['value'] += 50
                    logger.info(f"score {global_score['value']}")

        # Diag down right
        for r in range(3, rows):
            for c0 in range(cols - 3):
                diag = [board[r - i][c0 + i] for i in range(4)]
                if diag[:3] == [target] * 3 and diag[3] == ' ':
                    logger.info(f"[Open ↗ Triple] from ({r},{c0})")
                    global_score['value'] += 50
                    logger.info(f"score {global_score['value']}")
                elif diag[0] == ' ' and diag[1:] == [target] * 3:
                    logger.info(f"[Open ↗ Triple] ending at ({r-3},{c0+3})")
                    global_score['value'] += 50
                    logger.info(f"score {global_score['value']}")

        ### Opponent open triple

        # Horizontal
        for r in range(rows):
            for c0 in range(cols - 3):
                window = [board[r][c0 + i] for i in range(4)]
                if (window[:3] == [opponent] * 3 and window[3] == ' ') or \
                (window[0] == ' ' and window[1:] == [opponent] * 3):
                    logger.info(f"[Opponent Open Horizontal Triple] at row {r}, col {c0}")
                    global_score['value'] += -75
                    logger.info(f"score {global_score['value']}")

        # Vertical
        for r in range(rows - 3):
            for c0 in range(cols):
                if (board[r][c0] == opponent and
                    board[r + 1][c0] == opponent and
                    board[r + 2][c0] == opponent and
                    board[r + 3][c0] == ' '):
                    logger.info(f"[Opponent Open Vertical Triple] at col {c0}, starting row {r}")
                    global_score['value'] += -75
                    logger.info(f"score {global_score['value']}")

        #Diag down left
        for r in range(rows - 3):
            for c0 in range(cols - 3):
                diag = [board[r + i][c0 + i] for i in range(4)]
                if diag[:3] == [opponent] * 3 and diag[3] == ' ':
                    logger.info(f"[Opponent Open ↘ Triple] from ({r},{c0})")
                    global_score['value'] += -75
                    logger.info(f"score {global_score['value']}")
                elif diag[0] == ' ' and diag[1:] == [opponent] * 3:
                    logger.info(f"[Opponent Open ↘ Triple] ending at ({r+3},{c0+3})")
                    global_score['value'] += -75
                    logger.info(f"score {global_score['value']}")
        
        #Diag down right
        for r in range(3, rows):
            for c0 in range(cols - 3):
                diag = [board[r - i][c0 + i] for i in range(4)]
                if diag[:3] == [opponent] * 3 and diag[3] == ' ':
                    logger.info(f"[Opponent Open ↗ Triple] from ({r},{c0})")
                    global_score['value'] += -75
                    logger.info(f"score {global_score['value']}")
                elif diag[0] == ' ' and diag[1:] == [opponent] * 3:
                    logger.info(f"[Opponent Open ↗ Triple] ending at ({r-3},{c0+3})")
                    global_score['value'] += -75
                    logger.info(f"score {global_score['value']}")

        ### EARLY GAME/POSITIONING RULES

        # Center column priority
        if board[0][center_col] == ' ':
            logger.info(f"[Favor Center Column] col = {center_col}")
            global_score['value'] += 20
            logger.info(f"score {global_score['value']}")

        # Prioritize center positioning
        for offset in [1, -1]:
            near_col = center_col + offset
            if 0 <= near_col < cols and board[0][near_col] == ' ':
                logger.info(f"[Favor Near-Center Column] col = {near_col}")
                global_score['value'] += 10
                logger.info(f"score {global_score['value']}")

        # Avoid edges
        if board[0][0] == ' ':
            logger.info("[Penalize Edge Column] col = 0")
            global_score['value'] += -15
            logger.info(f"score {global_score['value']}")

        if board[0][cols - 1] == ' ':
            logger.info(f"[Penalize Edge Column] col = {cols - 1}")
            global_score['value'] += -15
            logger.info(f"score {global_score['value']}")

        # Prioritize center stacking
        for r in range(1, rows):
            if board[r][center_col] == target and board[r - 1][center_col] == ' ':
                logger.info(f"[Stack in Center Column] at row = {r - 1}")
                global_score['value'] += 25
                logger.info(f"score {global_score['value']}")
        
        # Avoid stacking pointless columns
        for c0 in range(cols):
            for r in range(rows):
                if board[r][c0] == ' ':
                    # count how many slots below this one
                    remaining = rows - r
                    if remaining < 4:
                        logger.info(f"[Penalize High Stack] at col = {c0}, row = {r}")
                        global_score['value'] += -10
                        logger.info(f"score {global_score['value']}")
                    break  # only check first empty row in column

### ============= ADD MORE RULES HERE ================= ###
### =================================================== ###
    @when_all(
        (m.type == 'cell')
    )
    def catch_all(c):
        # This just absorbs unmatched facts so they don't cause MessageNotHandledException
        pass
# --- Inference Functions ---------------------------------------------------------------

def set_player_symbol(symbol):
    """Sets the global player symbol for inference."""
    global my_game_symbol
    my_game_symbol = symbol

def board_to_facts(board, target):
    """Posts a context fact and converts the board into cell facts."""

    post('connect4', {
        'type': 'board',
        'board': board,
        'target': target
    })



def get_board_score():
    """Collects all score facts and returns total score."""
    return global_score['value']


# --- Fact Reset Utility ---

def reset_facts():
    """Safely retracts all facts from the 'connect4' ruleset if it exists."""
    global_score['value'] = 0
    host = get_host()
    try:
        try:
            facts = host.get_facts('connect4')
        except Exception:
            # Ruleset doesn't have any facts or is uninitialized
            return

        for fact in facts:
            host.retract_fact('connect4', fact)
    except Exception as e:
        print(f"[Warning] Could not reset facts: {e}")
