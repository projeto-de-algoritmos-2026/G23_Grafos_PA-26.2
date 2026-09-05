import math

# Distâncias puras de grid (não conhecem o custo do terreno). São admissíveis
# porque o terreno mais barato do grid custa 1 — nenhuma delas superestima o
# custo real restante. Em ordem de quão informadas são para movimento em 4
# direções: Manhattan (exata em número de passos) > Euclidiana > Chebyshev.


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a: tuple[int, int], b: tuple[int, int]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def chebyshev(a: tuple[int, int], b: tuple[int, int]) -> float:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


HEURISTICS = [
    ("Manhattan", manhattan),
    ("Euclidiana", euclidean),
    ("Chebyshev", chebyshev),
]
