"""Tile definitions."""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

TILE_DTYPE = np.dtype(
    [
        ("ch", np.intc),
        ("fg", "3B"),
        ("bg", "3B"),
        ("move_cost", np.intc),
        ("transparent", np.bool),
    ]
)
"""Data type for tile database."""


class NewTile(NamedTuple):
    """Helper class for new tiles."""

    ch: int
    fg: tuple[int, int, int] = (255, 255, 255)
    bg: tuple[int, int, int] = (0, 0, 0)
    move_cost: int = 0
    transparent: bool = False


TILES = np.array(
    [
        NewTile(ch=(ord(" ")), bg=(0x80, 0x80, 0x80), move_cost=1, transparent=True),
        NewTile(ch=(ord(".")), fg=(0x40, 0x40, 0x40), bg=(0, 0, 0)),
    ],
    dtype=TILE_DTYPE,
)
"""Tile database."""
