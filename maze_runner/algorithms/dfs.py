from .common import NEIGHBOR_OFFSETS, reconstruct_path


def dfs_steps(grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
    """Mesma estrutura do BFS, trocando a fila (FIFO) por uma pilha (LIFO) —
    acha *um* caminho, sem garantia de ser curto nem barato."""
    cols, rows = len(grid[0]), len(grid)
    visited = {start}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    stack = [start]
    order: list[tuple[int, int]] = []

    while stack:
        current = stack.pop()
        order.append(current)
        if current == end:
            break
        cx, cy = current
        for dx, dy in NEIGHBOR_OFFSETS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = current
                stack.append((nx, ny))
        yield order, set(stack), set(visited)

    yield order, set(), set(visited), reconstruct_path(parent, start, end)
