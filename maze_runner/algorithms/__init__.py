from .astar import astar_steps
from .bfs import bfs_steps
from .dfs import dfs_steps
from .dijkstra import dijkstra_steps
from .heuristics import HEURISTICS


def _astar_variant(heuristic):
    def steps_fn(grid, start, end):
        return astar_steps(grid, start, end, heuristic)

    return steps_fn


_ASTAR_HINTS = {
    "Manhattan": "ótimo · heurística exata p/ grade",
    "Euclidiana": "ótimo · heurística em linha reta",
    "Chebyshev": "ótimo · heurística mais fraca",
}

ALGORITHMS = [
    {"name": "BFS", "hint": "menos passos · ignora custo", "steps_fn": bfs_steps},
    {"name": "DFS", "hint": "só acha *um* caminho", "steps_fn": dfs_steps},
    {"name": "Dijkstra", "hint": "custo ótimo · sem heurística", "steps_fn": dijkstra_steps},
] + [
    {"name": f"A* ({heuristic_name})", "hint": _ASTAR_HINTS[heuristic_name], "steps_fn": _astar_variant(fn)}
    for heuristic_name, fn in HEURISTICS
]
