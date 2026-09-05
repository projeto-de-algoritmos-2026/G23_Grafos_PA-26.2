from ..grid import NEIGHBOR_OFFSETS

__all__ = ["NEIGHBOR_OFFSETS", "reconstruct_path"]


def reconstruct_path(
    parent: dict[tuple[int, int], tuple[int, int]], start: tuple[int, int], end: tuple[int, int]
) -> list[tuple[int, int]]:
    if end != start and end not in parent:
        return []
    path = []
    node = end
    while node in parent:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()
    return path
