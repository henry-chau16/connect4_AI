# inference.py — Durable Rules Based Inference Engine for Connect 4

import logging

# Setup logging for rules fired
logging.basicConfig(
    filename='inference_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)


### ------- REASONING SEGMENT ------- ###
### --------------------------------- ###

from durable.lang import ruleset, when_all, post, get_host, m

# === RULE BASE ======================================================================== #

with ruleset('connect4'):

    ### OFFENSIVE (SCORING) RULES ### --------------------------------------------------

    ## Winning rules (4 in a row): score: +1000 (Always go for win)
    #  4 rules for each direction (horizontal, vertical, down-left diagonal, down-right diagonal)

    # horizontal
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value == m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row) & (m.col == m.f1.col + 3)
    )
    def win_horizontal(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Winning horizontal pattern starting at ({col}, {row})")
        c.assert_fact('score', {'value': 1000})

    # vertical
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value == m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.target) & (m.col == m.f1.col) & (m.row == m.f1.row + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.target) & (m.col == m.f1.col) & (m.row == m.f1.row + 2),
        m.f4 << (m.type == 'cell') & (m.value == m.f1.target) & (m.col == m.f1.col) & (m.row == m.f1.row + 3)
    )
    def win_vertical(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Winning vertical pattern starting at ({col}, {row})")
        c.assert_fact('score', {'value': 1000})

    # diagonal (down-left)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value == m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row + 1) & (m.col == m.f1.col - 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row + 2) & (m.col == m.f1.col - 2),
        m.f4 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row + 3) & (m.col == m.f1.col - 3)
    )
    def win_diag_dl(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Winning diagonal starting at ({row}, {col})")
        c.assert_fact('score', {'value': 1000})

    # diagonal (down-right)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value == m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row + 1) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row + 2) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row + 3) & (m.col == m.f1.col + 3)
    )
    def win_diag_dr(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"🏆 Winning diagonal starting at ({row}, {col})")
        c.assert_fact('score', {'value': 1000})


    ## Open triple rules (3 in a row with unblocked 4th): score: +50 (high priority)
    #  4 rules for each direction (horizontal, vertical, down-left diagonal, down-right diagonal)

    # horizontal
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value == m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row) & (m.col == m.f1.col + 3)
    )
    def open_triple_horizontal(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Detected open triple starting at ({col}, {row})")
        c.assert_fact('score', {'value': 50})

    ### DEFENSIVE (BLOCK AND TANGLE) RULES ### -----------------------------------------------

    ## Opponent win rules (Opponent 4 in a row): score: -1000 (Must avoid)
    #  4 rules for each direction (horizontal, vertical, down-left diagonal, down-right diagonal)

    # horizontal
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row) & (m.col == m.f1.col + 3)
    )
    def lose_horizontal(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Opponent horizontal win detected starting at ({col}, {row})")
        c.assert_fact('score', {'value': -1000})

    # vertical
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.col == m.f1.col) & (m.row == m.f1.row + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.col == m.f1.col) & (m.row == m.f1.row + 2),
        m.f4 << (m.type == 'cell') & (m.value == m.f1.value) & (m.col == m.f1.col) & (m.row == m.f1.row + 3)
    )
    def lose_vertical(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Opponent vertical win detected at col {col}, row {row}")
        c.assert_fact('score', {'value': -1000})

    # diagonal (down-left)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 1) & (m.col == m.f1.col - 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 2) & (m.col == m.f1.col - 2),
        m.f4 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 3) & (m.col == m.f1.col - 3)
    )
    def lose_diag_dl(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Opponent diagonal win starting at ({row}, {col})")
        c.assert_fact('score', {'value': -1000})

    # diagonal (down-right)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 1) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 2) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 3) & (m.col == m.f1.col + 3)
    )
    def lose_diag_dr(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Opponent diagonal win starting at ({row}, {col})")
        c.assert_fact('score', {'value': -1000})

    ## Opponent open triple rules (Opponent 3 in a row with unblocked 4th): score: -70 (Must block)
    #  4 rules for each direction (horizontal, vertical, down-left diagonal, down-right diagonal)

    # horizontal
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row) & (m.col == m.f1.col + 3)
    )
    def block_opponent_horizontal_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Detected opponent open triple starting at ({col}, {row})")
        c.assert_fact('score', {'value': -70})
    
    # vertical
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.col == m.f1.col) & (m.row == m.f1.row + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.col == m.f1.col) & (m.row == m.f1.row + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.col == m.f1.col) & (m.row == m.f1.row + 3)
    )
    def block_opponent_vertical_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Detected opponent open triple starting at ({col}, {row})")
        c.assert_fact('score', {'value': -70})
    
    # diagonal (down-left)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 1) & (m.col == m.f1.col - 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 2) & (m.col == m.f1.col - 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row + 3) & (m.col == m.f1.col - 3)
    )
    def block_opponent_diag_dl_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Detected opponent open triple starting at ({col}, {row})")
        c.assert_fact('score', {'value': -70})

    # diagonal (down-right)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 1) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 2) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row + 3) & (m.col == m.f1.col + 3)
    )
    def block_opponent_diag_dr_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        logger.info(f"Detected opponent open triple starting at ({col}, {row})")
        c.assert_fact('score', {'value': -70})

    ### EARLY GAME (PLAY FOR GOOD POSITIONING AND SETUP) RULES ### -----------------------------------------------
    
    ## TODO: ADD EARLY GAME RULES ##


### ============= ADD MORE RULES HERE ================= ###
### =================================================== ###

# --- Inference Functions ---------------------------------------------------------------

def set_player_symbol(symbol):
    """Sets the global player symbol for inference."""
    global my_game_symbol
    my_game_symbol = symbol

def board_to_facts(board):
    """Converts a board into facts, using the current player symbol."""
    for r, row in enumerate(board):
        for c, val in enumerate(row):
            post('connect4', {
                'type': 'cell',
                'row': r,
                'col': c,
                'value': val,
                'target': my_game_symbol  # dynamic match symbol
            })

def get_board_score():
    """Collects all score facts and returns total score."""

    logger.info("===================== Evaluating board =========================")
    host = get_host()
    score_facts = host.get_facts('score')
    total = sum(f['value'] for f in score_facts)
    logger.info(f"--------------------- SCORE: {total} -------------------------")
    return total


# --- Fact Reset Utility ---

def reset_facts():
    """Retracts all facts from the 'connect4' ruleset."""
    host = get_host()
    try:
        facts = host.get_facts('connect4')
        for fact in facts:
            host.retract_fact('connect4', fact)
    except Exception as e:
        print(f"[Warning] Could not reset facts: {e}")