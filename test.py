import Team1_Connect_4_Agent as t1

cols = 6
rows = 7

board = [[' ' for _ in range(cols)] for _ in range(rows)]

t1.init_agent('X', rows, cols, board)

print(t1.what_is_your_move(board, rows, cols, 'X'))