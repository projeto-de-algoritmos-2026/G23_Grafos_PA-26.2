import heapq
from typing import Callable

from .common import NEIGHBOR_OFFSETS, reconstruct_path

Heuristic = Callable[[tuple[int, int], tuple[int, int]], float]


def astar_steps(grid: list[list[int]], start: tuple[int, int], end: tuple[int, int], heuristic: Heuristic):
    """Como Dijkstra, mas prioriza custo acumulado + estimativa até o fim
    (heurística) — expande menos nós quanto mais informada for a heurística."""
    cols, rows = len(grid[0]), len(grid)
    g_score = {start: 0}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    visited: set[tuple[int, int]] = set()
    frontier: set[tuple[int, int]] = {start}
    order: list[tuple[int, int]] = []
    heap: list[tuple[float, tuple[int, int]]] = [(heuristic(start, end), start)]

    while heap:
        _, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        frontier.discard(current)
        order.append(current)
        if current == end:
            break
        cx, cy = current
        for dx, dy in NEIGHBOR_OFFSETS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != 0:
                tentative_g = g_score[current] + grid[ny][nx]
                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = tentative_g
                    parent[(nx, ny)] = current
                    heapq.heappush(heap, (tentative_g + heuristic((nx, ny), end), (nx, ny)))
                    frontier.add((nx, ny))
        yield order, set(frontier), set(visited)

    yield order, set(), set(visited), reconstruct_path(parent, start, end)
