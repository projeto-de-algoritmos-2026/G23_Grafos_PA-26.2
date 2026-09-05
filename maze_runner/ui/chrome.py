"""Elementos visuais decorativos compartilhados entre as telas: cantos estilo
HUD, texto com tracking manual, fundo quadriculado e a linha pontilhada usada
no menu (estilo índice/sumário técnico)."""

import pygame

from . import colors


def tracked_text(font: pygame.font.Font, text: str, color: tuple[int, int, int], tracking: int = 3) -> pygame.Surface:
    glyphs = [font.render(ch, True, color) for ch in text]
    total_w = sum(g.get_width() for g in glyphs) + tracking * max(len(glyphs) - 1, 0)
    height = font.get_height()
    out = pygame.Surface((max(total_w, 1), height), pygame.SRCALPHA)
    x = 0
    for g in glyphs:
        out.blit(g, (x, 0))
        x += g.get_width() + tracking
    return out


def draw_corner_brackets(
    screen: pygame.Surface,
    color: tuple[int, int, int] = colors.ACCENT_DIM,
    size: int = 18,
    thickness: int = 2,
    margin: int = 12,
) -> None:
    w, h = screen.get_size()
    for (x, y), (sx, sy) in (
        ((margin, margin), (1, 1)),
        ((w - margin, margin), (-1, 1)),
        ((margin, h - margin), (1, -1)),
        ((w - margin, h - margin), (-1, -1)),
    ):
        pygame.draw.line(screen, color, (x, y), (x + size * sx, y), thickness)
        pygame.draw.line(screen, color, (x, y), (x, y + size * sy), thickness)


def draw_grid_background(screen: pygame.Surface, spacing: int = 28) -> None:
    w, h = screen.get_size()
    for x in range(0, w, spacing):
        pygame.draw.line(screen, colors.BG_GRID_LINE, (x, 0), (x, h), 1)
    for y in range(0, h, spacing):
        pygame.draw.line(screen, colors.BG_GRID_LINE, (0, y), (w, y), 1)


def draw_leader_row(
    screen: pygame.Surface,
    font: pygame.font.Font,
    x: int,
    y: int,
    left: str,
    right: str,
    right_edge: int,
    left_color: tuple[int, int, int] = colors.TEXT,
    right_color: tuple[int, int, int] = colors.TEXT_DIM,
) -> None:
    """Linha estilo índice: 'texto ......... valor', alinhado à direita."""
    left_surf = font.render(left, True, left_color)
    right_surf = font.render(right, True, right_color)
    screen.blit(left_surf, (x, y))
    right_x = right_edge - right_surf.get_width()
    screen.blit(right_surf, (right_x, y))

    dot_y = y + left_surf.get_height() // 2
    dot_start = x + left_surf.get_width() + 10
    dot_end = right_x - 10
    xx = dot_start
    while xx < dot_end:
        pygame.draw.rect(screen, colors.TEXT_FAINT, pygame.Rect(int(xx), dot_y, 2, 2))
        xx += 6
