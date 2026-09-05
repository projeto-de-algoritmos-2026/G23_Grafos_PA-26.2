import random
from collections import deque

WALL = 0
NEIGHBOR_OFFSETS = ((1, 0), (-1, 0), (0, 1), (0, -1))

# (custo, peso de sorteio) — a maioria do grid é terreno plano, com bolsões
# mais caros de lama e água espalhados.
TERRAIN_WEIGHTS = [(1, 0.65), (3, 0.25), (5, 0.10)]


def _is_connected(grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> bool:
    cols, rows = len(grid[0]), len(grid)
    seen = {start}
    queue = deque([start])
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == end:
            return True
        for dx, dy in NEIGHBOR_OFFSETS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != WALL and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append((nx, ny))
    return False


def generate_maze(
    cols: int, rows: int, start: tuple[int, int], end: tuple[int, int], wall_probability: float
) -> list[list[int]]:
    """0 = parede. Célula livre guarda o custo de entrar nela (terreno) — é
    esse custo que faz Dijkstra e A* divergirem de BFS/DFS de verdade."""
    costs, weights = zip(*TERRAIN_WEIGHTS)
    while True:
        grid = [
            [
                WALL if random.random() < wall_probability else random.choices(costs, weights=weights)[0]
                for _ in range(cols)
            ]
            for _ in range(rows)
        ]
        grid[start[1]][start[0]] = 1
        grid[end[1]][end[0]] = 1
        if _is_connected(grid, start, end):
            return grid


def path_cost(grid: list[list[int]], path: list[tuple[int, int]]) -> int:
    return sum(grid[y][x] for x, y in path[1:])
