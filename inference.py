# inference.py — Durable Rules Based Inference Engine for Connect 4

### ------- REASONING SEGMENT ------- ###
### --------------------------------- ###

from durable.lang import ruleset, when_all, post, get_host, m

# --- Rule Definitions ---

with ruleset('connect4'):

    # Rule: Detect horizontal open triple (generic)
    @when_all(
        m.f1 << (m.type == 'cell') & (m.value == 'X'),
        m.f2 << (m.type == 'cell') & (m.value == 'X') & (m.row == m.f1.row) & (m.col == m.f1.col + 1),
        m.f3 << (m.type == 'cell') & (m.value == 'X') & (m.row == m.f1.row) & (m.col == m.f1.col + 2),
        m.f4 << (m.type == 'cell') & (m.value == ' ') & (m.row == m.f1.row) & (m.col == m.f1.col + 3)
    )
    def open_triple(c):
        row = c.m.f1['row']
        col = c.m.f1['col']
        print(f"Detected open triple at row {row}, starting col {col}")
        c.assert_fact('score', {'value': 50})


### ============= ADD MORE RULES HERE ================= ###
### =================================================== ###

# --- Inference Functions ---

def board_to_facts(board, player_symbol):
    """Converts a board into durable rules facts."""
    for r, row in enumerate(board):
        for c, val in enumerate(row):
            post('connect4', {
                'type': 'cell',
                'row': r,
                'col': c,
                'value': val
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
