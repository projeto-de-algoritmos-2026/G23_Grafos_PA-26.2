import pygame

from .. import config
from . import chrome, colors, fonts

EYEBROW = fonts.mono("Medium", 13)
TITLE = fonts.mono("Bold", 26)
OPTION = fonts.mono("Regular", 16)
OPTION_NUM = fonts.mono("SemiBold", 16)
TAG = fonts.mono("Regular", 13)
HINT = fonts.mono("Regular", 13)
BADGE = fonts.mono("Bold", 14)

CONTENT_LEFT = config.MARGIN
CONTENT_RIGHT = config.WIDTH - config.MARGIN


def _chip(screen: pygame.Surface, x: int, y: int, text: str, active: bool = False) -> int:
    """Desenha um numero dentro de uma caixinha com borda; devolve a largura usada."""
    pad_x, pad_y = 10, 6
    label = OPTION_NUM.render(text, True, colors.BG if active else colors.ACCENT)
    w = label.get_width() + pad_x * 2
    h = label.get_height() + pad_y * 2
    rect = pygame.Rect(x, y, w, h)
    if active:
        pygame.draw.rect(screen, colors.ACCENT, rect, border_radius=3)
    else:
        pygame.draw.rect(screen, colors.PANEL_BORDER, rect, border_radius=3)
        pygame.draw.rect(screen, colors.ACCENT_DIM, rect, width=1, border_radius=3)
    screen.blit(label, (x + pad_x, y + pad_y))
    return w


def _header(screen: pygame.Surface, eyebrow: str, title: str) -> int:
    screen.blit(chrome.tracked_text(EYEBROW, eyebrow, colors.ACCENT, tracking=4), (CONTENT_LEFT, 34))
    screen.blit(TITLE.render(title, True, colors.TEXT), (CONTENT_LEFT, 56))
    divider_y = 100
    pygame.draw.line(screen, colors.PANEL_BORDER, (CONTENT_LEFT, divider_y), (CONTENT_RIGHT, divider_y), 1)
    pygame.draw.line(screen, colors.ACCENT, (CONTENT_LEFT, divider_y), (CONTENT_LEFT + 48, divider_y), 2)
    return divider_y


def _footer(screen: pygame.Surface, text: str) -> None:
    y = config.HEIGHT - 40
    pygame.draw.line(screen, colors.PANEL_BORDER, (CONTENT_LEFT, y), (CONTENT_RIGHT, y), 1)
    screen.blit(HINT.render(text, True, colors.TEXT_DIM), (CONTENT_LEFT, y + 12))


def draw_menu(screen: pygame.Surface, algorithms: list[dict]) -> None:
    screen.fill(colors.BG)
    chrome.draw_grid_background(screen)
    chrome.draw_corner_brackets(screen)

    y = _header(screen, "MAZE RUNNER // SELECIONAR ALGORITMO", "Escolha o que vai resolver o labirinto") + 34

    for i, algo in enumerate(algorithms, start=1):
        chip_w = _chip(screen, CONTENT_LEFT, y, str(i))
        text_x = CONTENT_LEFT + chip_w + 16
        chrome.draw_leader_row(screen, OPTION, text_x, y + 5, algo["name"], algo["hint"], CONTENT_RIGHT)
        y += 40

    y += 14
    pygame.draw.line(screen, colors.PANEL_BORDER, (CONTENT_LEFT, y), (CONTENT_RIGHT, y), 1)
    y += 22

    chip_w = _chip(screen, CONTENT_LEFT, y, "T", active=True)
    label = chrome.tracked_text(OPTION_NUM, "RODAR TODOS EM SEQUÊNCIA", colors.ACCENT, tracking=2)
    screen.blit(label, (CONTENT_LEFT + chip_w + 16, y + 5))
    tag = TAG.render("gera o ranking comparativo no final", True, colors.TEXT_DIM)
    screen.blit(tag, (CONTENT_RIGHT - tag.get_width(), y + 6))

    _footer(screen, f"ESC  sair          seed do labirinto: {config.MAZE_SEED}   ·   grade {config.COLS}×{config.ROWS}")


def draw_ranking(screen: pygame.Surface, results: list[dict]) -> None:
    screen.fill(colors.BG)
    chrome.draw_grid_background(screen)
    chrome.draw_corner_brackets(screen)

    y = _header(screen, "MAZE RUNNER // RESULTADOS", "Ranking comparativo") + 30

    # colunas na mesma ordem de prioridade do critério de desempate do ranking
    col_algo, col_cost, col_time, col_steps, col_nodes = (
        CONTENT_LEFT + 60,
        CONTENT_LEFT + 300,
        CONTENT_LEFT + 400,
        CONTENT_LEFT + 500,
        CONTENT_LEFT + 600,
    )
    header_y = y
    for label, x in (("ALGORITMO", col_algo), ("CUSTO", col_cost), ("TEMPO", col_time), ("PASSOS", col_steps), ("NÓS", col_nodes)):
        screen.blit(chrome.tracked_text(TAG, label, colors.TEXT_DIM, tracking=2), (x, header_y))
    y += 26
    pygame.draw.line(screen, colors.PANEL_BORDER, (CONTENT_LEFT, y), (CONTENT_RIGHT, y), 1)
    y += 12

    # prioridade: custo mais baixo primeiro; empate quebrado por tempo, depois
    # passos, depois nós expandidos.
    ranked = sorted(results, key=lambda r: (r["cost"], r["time_s"], r["path_len"], r["nodes"]))
    for place, r in enumerate(ranked, start=1):
        row_rect = pygame.Rect(CONTENT_LEFT - 6, y - 4, CONTENT_RIGHT - CONTENT_LEFT + 12, 30)
        if place % 2 == 0:
            pygame.draw.rect(screen, (14, 18, 25), row_rect, border_radius=3)

        is_first = place == 1
        badge_color = colors.ACCENT if is_first else colors.PANEL_BORDER
        badge_text_color = colors.BG if is_first else colors.TEXT_DIM
        badge = BADGE.render(f"{place}", True, badge_text_color)
        badge_rect = pygame.Rect(CONTENT_LEFT, y - 3, 26, 26)
        pygame.draw.rect(screen, badge_color, badge_rect, border_radius=3)
        screen.blit(badge, badge.get_rect(center=badge_rect.center))

        name_color = colors.TEXT if is_first else colors.TEXT_DIM
        screen.blit(OPTION.render(r["name"], True, name_color), (col_algo, y))
        screen.blit(OPTION.render(str(r["cost"]), True, name_color), (col_cost, y))
        screen.blit(OPTION.render(f"{r['time_s']:.2f}s", True, name_color), (col_time, y))
        screen.blit(OPTION.render(str(r["path_len"]), True, name_color), (col_steps, y))
        screen.blit(OPTION.render(str(r["nodes"]), True, name_color), (col_nodes, y))
        y += 34

    _footer(screen, "ENTER  voltar ao menu          ESC  sair")
