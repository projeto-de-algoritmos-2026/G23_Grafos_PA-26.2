import time

import pygame

from .. import config
from ..grid import path_cost
from . import chrome, colors, fonts

EYEBROW = fonts.mono("Medium", 13)
TITLE = fonts.mono("Bold", 22)
STAT_LABEL = fonts.mono("Regular", 12)
STAT_VALUE = fonts.mono("SemiBold", 15)
LEGEND = fonts.mono("Regular", 12)


def cell_rect(x: int, y: int) -> pygame.Rect:
    return pygame.Rect(
        config.MARGIN + x * config.CELL + 1,
        config.HEADER + config.MARGIN + y * config.CELL + 1,
        config.CELL - 2,
        config.CELL - 2,
    )


def draw_cell(screen: pygame.Surface, x: int, y: int, color: tuple[int, int, int]) -> None:
    pygame.draw.rect(screen, color, cell_rect(x, y), border_radius=5)


def draw_terrain_legend(screen: pygame.Surface) -> None:
    x, y = config.WIDTH - 150, 20
    for cost, label in ((1, "custo 1"), (3, "custo 3"), (5, "custo 5")):
        pygame.draw.rect(screen, colors.TERRAIN_COLORS[cost], pygame.Rect(x, y, 12, 12), border_radius=3)
        screen.blit(LEGEND.render(label, True, colors.TEXT_DIM), (x + 18, y - 2))
        y += 20


def _stat(screen: pygame.Surface, x: int, y: int, label: str, value: str) -> int:
    screen.blit(chrome.tracked_text(STAT_LABEL, label, colors.TEXT_DIM, tracking=2), (x, y))
    screen.blit(STAT_VALUE.render(value, True, colors.TEXT), (x, y + 18))
    return x


class Run:
    """Estado de uma execução de algoritmo em andamento: busca animada,
    revelação do caminho e as métricas usadas depois no ranking."""

    def __init__(self, name: str, steps_fn, grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
        self.name = name
        self.grid = grid
        self.start = start
        self.end = end
        self.steps = steps_fn(grid, start, end)
        self.visited_order: list[tuple[int, int]] = []
        self.frontier: set[tuple[int, int]] = set()
        self.visited: set[tuple[int, int]] = set()
        self.path: list[tuple[int, int]] = []
        self.cost = 0
        self.phase = "searching"  # searching -> revealing -> done
        self.reveal_count = 0
        self.anim_start = time.perf_counter()
        self.anim_elapsed_s = 0.0
        self.done_at: float | None = None

    def tick(self) -> None:
        if self.phase == "searching":
            for _ in range(config.SEARCH_STEPS_PER_FRAME):
                try:
                    state = next(self.steps)
                except StopIteration:
                    self._finish_search()
                    break
                if len(state) == 4:
                    self.visited_order, self.frontier, self.visited, self.path = state
                    self._finish_search()
                    break
                self.visited_order, self.frontier, self.visited = state
        elif self.phase == "revealing":
            self.reveal_count = min(len(self.path), self.reveal_count + config.REVEAL_CELLS_PER_FRAME)
            if self.reveal_count >= len(self.path):
                self.phase = "done"
                self.done_at = time.perf_counter()

    def _finish_search(self) -> None:
        self.phase = "revealing"
        self.anim_elapsed_s = time.perf_counter() - self.anim_start
        self.cost = path_cost(self.grid, self.path) if self.path else 0

    def draw(self, screen: pygame.Surface) -> None:
        rows, cols = len(self.grid), len(self.grid[0])
        screen.fill(colors.BG)
        chrome.draw_corner_brackets(screen)

        searching = self.phase == "searching"
        eyebrow = "MAZE RUNNER // BUSCANDO" if searching else "MAZE RUNNER // RESOLVIDO"
        screen.blit(chrome.tracked_text(EYEBROW, eyebrow, colors.ACCENT, tracking=4), (config.MARGIN, 14))
        screen.blit(TITLE.render(self.name, True, colors.TEXT), (config.MARGIN, 34))

        shown_elapsed = (time.perf_counter() - self.anim_start) if searching else self.anim_elapsed_s
        stats_y = 74
        x = config.MARGIN
        x = _stat(screen, x, stats_y, "NÓS EXPANDIDOS", str(len(self.visited_order))) + 150
        x = _stat(screen, x, stats_y, "TEMPO", f"{shown_elapsed:.2f}s") + 110
        if not searching:
            x = _stat(screen, x, stats_y, "PASSOS", str(len(self.path))) + 90
            _stat(screen, x, stats_y, "CUSTO", str(self.cost))

        for y in range(rows):
            for x_ in range(cols):
                if self.grid[y][x_] != 0:
                    draw_cell(screen, x_, y, colors.TERRAIN_COLORS[self.grid[y][x_]])

        if searching:
            for pos in self.visited:
                draw_cell(screen, *pos, colors.VISITED)
            for pos in self.frontier:
                draw_cell(screen, *pos, colors.FRONTIER)
        else:
            for pos in self.path[: self.reveal_count]:
                draw_cell(screen, *pos, colors.PATH)

        draw_cell(screen, *self.start, colors.START)
        draw_cell(screen, *self.end, colors.END)

        draw_terrain_legend(screen)
