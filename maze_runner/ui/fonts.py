from pathlib import Path

import pygame

pygame.font.init()

_FONT_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"
_cache: dict[tuple[str, int], pygame.font.Font] = {}


def mono(weight: str, size: int) -> pygame.font.Font:
    """weight: Regular | Medium | SemiBold | Bold (IBM Plex Mono)."""
    key = (weight, size)
    if key not in _cache:
        _cache[key] = pygame.font.Font(str(_FONT_DIR / f"IBMPlexMono-{weight}.ttf"), size)
    return _cache[key]
