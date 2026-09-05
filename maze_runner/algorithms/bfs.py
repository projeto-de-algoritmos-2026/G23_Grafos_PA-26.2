from collections import deque

from .common import NEIGHBOR_OFFSETS, reconstruct_path


def bfs_steps(grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    """Explora por número de passos, ignorando o custo do terreno — por isso
    acha o caminho mais curto em passos, não necessariamente o mais barato."""
    cols, rows = len(grid[0]), len(grid)
    visited = {start}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    queue = deque([start])
    order: list[tuple[int, int]] = []

    while queue:
        current = queue.popleft()
        order.append(current)
        if current == end:
            break
        cx, cy = current
        for dx, dy in NEIGHBOR_OFFSETS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = current
                queue.append((nx, ny))
        yield order, set(queue), set(visited)

    yield order, set(), set(visited), reconstruct_path(parent, start, end)
