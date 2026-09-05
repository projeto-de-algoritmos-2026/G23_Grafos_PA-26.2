import heapq

from .common import NEIGHBOR_OFFSETS, reconstruct_path


def dijkstra_steps(grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    """Expande sempre o nó de menor custo acumulado (fila de prioridade), então
    o caminho encontrado é o mais barato de verdade, considerando o terreno."""
    cols, rows = len(grid[0]), len(grid)
    dist = {start: 0}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    visited: set[tuple[int, int]] = set()
    frontier: set[tuple[int, int]] = {start}
    order: list[tuple[int, int]] = []
    heap: list[tuple[int, tuple[int, int]]] = [(0, start)]

    while heap:
        d, current = heapq.heappop(heap)
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
                nd = d + grid[ny][nx]
                if (nx, ny) not in dist or nd < dist[(nx, ny)]:
                    dist[(nx, ny)] = nd
                    parent[(nx, ny)] = current
                    heapq.heappush(heap, (nd, (nx, ny)))
                    frontier.add((nx, ny))
        yield order, set(frontier), set(visited)

    yield order, set(), set(visited), reconstruct_path(parent, start, end)
