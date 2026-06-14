"""Common map functions."""

from __future__ import annotations

import numpy as np
import tcod.constants
import tcod.map
from tcod.ecs import Entity

from components import MapShape, Memory, Position, Tiles, Visible
from tiles import TILE_DATA


def update_fov(pov: Entity) -> None:
    """Update a map's Visible and Memory layers."""
    pos = pov.components[Position]
    map_ = pov.relation_tag["IsIn"]

    map_.components[Visible] = tcod.map.compute_fov(
        transparency=TILE_DATA["transparent"][map_.components[Tiles]],
        pov=(pos.y, pos.x),
        radius=8,
        algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST,
    )

    if Memory not in map_.components:
        map_.components[Memory] = np.zeros(map_.components[MapShape], dtype=np.uint8)
    np.choose(
        map_.components[Visible],
        choices=[map_.components[Memory], map_.components[Tiles]],
        out=map_.components[Memory],
    )
