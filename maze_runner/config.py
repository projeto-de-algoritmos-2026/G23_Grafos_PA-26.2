COLS, ROWS = 40, 26
CELL = 20
MARGIN = 40
HEADER = 120
WALL_PROBABILITY = 0.22
MAZE_SEED = 42  # fixo: todo algoritmo precisa resolver o mesmo labirinto pro ranking valer

WIDTH = COLS * CELL + MARGIN * 2
HEIGHT = ROWS * CELL + MARGIN * 2 + HEADER

START_POS = (0, 0)
END_POS = (COLS - 1, ROWS - 1)

SEARCH_STEPS_PER_FRAME = 3
SEARCH_FPS = 40
REVEAL_CELLS_PER_FRAME = 2
REVEAL_FPS = 30
AUTO_ADVANCE_DELAY_S = 1.5  # pausa no modo "rodar todos" antes de ir pro próximo
