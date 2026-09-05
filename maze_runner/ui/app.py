import random
import time

import pygame

from .. import config
from ..algorithms import ALGORITHMS
from ..grid import generate_maze
from . import colors, fonts
from .run import Run
from .screens import draw_menu, draw_ranking

HINT_FONT = fonts.mono("Regular", 13)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Maze Runner")
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()

    random.seed(config.MAZE_SEED)
    grid = generate_maze(config.COLS, config.ROWS, config.START_POS, config.END_POS, config.WALL_PROBABILITY)

    state = "menu"  # menu -> running -> (ranking, só no modo "rodar todos") -> menu
    comparison_mode = False
    remaining_algos: list[dict] = []
    current_run: Run | None = None
    results: list[dict] = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif state == "menu":
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        if idx < len(ALGORITHMS):
                            comparison_mode = False
                            remaining_algos = []
                            results = []
                            algo = ALGORITHMS[idx]
                            current_run = Run(algo["name"], algo["steps_fn"], grid, config.START_POS, config.END_POS)
                            state = "running"
                    elif event.key == pygame.K_t:
                        comparison_mode = True
                        remaining_algos = list(ALGORITHMS[1:])
                        results = []
                        first = ALGORITHMS[0]
                        current_run = Run(first["name"], first["steps_fn"], grid, config.START_POS, config.END_POS)
                        state = "running"
                elif state == "ranking" and event.key == pygame.K_RETURN:
                    state = "menu"
                elif (
                    state == "running"
                    and event.key == pygame.K_RETURN
                    and current_run is not None
                    and current_run.phase == "done"
                    and not comparison_mode
                ):
                    state = "menu"

        if state == "running" and current_run is not None:
            current_run.tick()

            if current_run.phase == "done" and comparison_mode:
                ready = time.perf_counter() - current_run.done_at >= config.AUTO_ADVANCE_DELAY_S
                if ready:
                    results.append(
                        {
                            "name": current_run.name,
                            "time_s": current_run.anim_elapsed_s,
                            "nodes": len(current_run.visited_order),
                            "path_len": len(current_run.path),
                            "cost": current_run.cost,
                        }
                    )
                    if remaining_algos:
                        next_algo = remaining_algos.pop(0)
                        current_run = Run(
                            next_algo["name"], next_algo["steps_fn"], grid, config.START_POS, config.END_POS
                        )
                    else:
                        state = "ranking"

        if state == "menu":
            draw_menu(screen, ALGORITHMS)
        elif state == "running" and current_run is not None:
            current_run.draw(screen)
            if current_run.phase == "done":
                hint = (
                    "Próximo algoritmo em instantes..."
                    if comparison_mode
                    else "ENTER  voltar ao menu          ESC  sair"
                )
                y = config.HEIGHT - 40
                pygame.draw.line(screen, colors.PANEL_BORDER, (config.MARGIN, y), (config.WIDTH - config.MARGIN, y), 1)
                screen.blit(HINT_FONT.render(hint, True, colors.TEXT_DIM), (config.MARGIN, y + 12))
        elif state == "ranking":
            draw_ranking(screen, results)

        pygame.display.flip()
        fps = config.SEARCH_FPS if (current_run and current_run.phase == "searching") else config.REVEAL_FPS
        clock.tick(fps if state == "running" else 30)

    pygame.quit()
