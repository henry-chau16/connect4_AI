# inference.py — Durable Rules Based Inference Engine for Connect 4

### ------- REASONING SEGMENT ------- ###
### --------------------------------- ###

from durable.lang import ruleset, when_all, post, get_host, m

# --- RULE BASE ------------------------------------------------------------------------

with ruleset('connect4'):

    ### OFFENSIVE (SCORING) RULES ###

    ### TODO: ADD WINNING RULES (4 in a row, score = 1000 for each direction)

    # Rule: Detect horizontal open triple for the current player symbol
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value == m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.target) & (m.row == m.f1.row) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row) & (m.col == m.f1.col + 3)
    )
    def open_triple_horizontal(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        print(f"Detected open triple at row {row}, starting col {col}")
        c.assert_fact('score', {'value': 50})

    ### DEFENSIVE (BLOCK AND TANGLE) RULES ###

    ### TODO: ADD LOSING RULES (4 in a row for opponent, score = -1000 for each direction)

    # Rule: Block opponent horizontal triple
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row) & (m.col == m.f1.col + 3)
    )
    def block_opponent_horizontal_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        print(f"Opponent horizontal triple at row {row}, col {col}")
        c.assert_fact('score', {'value': -70})
    
    # Rule: Block opponent vertical triple
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.col == m.f1.col) & (m.row == m.f1.row + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.col == m.f1.col) & (m.row == m.f1.row + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.col == m.f1.col) & (m.row == m.f1.row + 3)
    )
    def block_opponent_vertical_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        print(f"Opponent vertical triple at col {col}, starting row {row}")
        c.assert_fact('score', {'value': -70})
    
    # Rule Block opponent diagonal triple (down left)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 1) & (m.col == m.f1.col - 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 2) & (m.col == m.f1.col - 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row + 3) & (m.col == m.f1.col - 3)
    )
    def block_opponent_diag_dl_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        print(f"Opponent down-left diagonal triple starting at ({row}, {col})")
        c.assert_fact('score', {'value': -70})

    # Rule Block opponent diagonal triple (down right)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value != ' ') & (m.value != m.f1.target),
        m.f2 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 1) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == m.f1.value) & (m.row == m.f1.row + 2) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row + 3) & (m.col == m.f1.col + 3)
    )
    def block_opponent_diag_dr_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        print(f"Opponent down-right diagonal triple starting at ({row}, {col})")
        c.assert_fact('score', {'value': -70})



### ============= ADD MORE RULES HERE ================= ###
### =================================================== ###

# --- Inference Functions ---------------------------------------------------------------

def set_player_symbol(symbol):
    """Sets the global player symbol for inference."""
    global my_game_symbol
    my_game_symbol = symbol

def board_to_facts(board):
    """Converts a board into durable rules facts, using the current player symbol."""
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
    host = get_host()
    score_facts = host.get_facts('score')
    total = sum(f['value'] for f in score_facts)
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