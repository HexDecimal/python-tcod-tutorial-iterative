"""Common rendering functions."""

from __future__ import annotations

import numpy as np
import tcod.camera
import tcod.console

import tiles
from components import Graphic, MapShape, Memory, Position, Tiles, Visible


def render_map(console: tcod.console.Console, camera: Position) -> None:
    """Render the map at `camera` to the `console`."""
    world = camera.z.registry
    pivot_x, pivot_y = camera.x - console.width // 2, camera.y - console.height // 2

    screen_slice, world_slice = tcod.camera.get_slices(
        screen=(console.height, console.width), world=camera.z.components[MapShape], camera=(pivot_y, pivot_x)
    )

    world_tiles = camera.z.components[Tiles][world_slice]
    console.rgb[screen_slice] = tiles.TILE_DATA[["ch", "fg", "bg"]][world_tiles]

    is_visible = camera.z.components[Visible]

    visible_tiles = tiles.TILE_DATA[["ch", "fg", "bg"]][world_tiles]
    memory_tiles = tiles.TILE_DATA[["ch", "fg", "bg"]][camera.z.components[Memory][world_slice]]
    memory_tiles["fg"] //= 2
    memory_tiles["bg"] //= 2

    console.rgb[screen_slice] = np.select(
        condlist=[is_visible[world_slice]], choicelist=[visible_tiles], default=memory_tiles
    )

    for entity in world.Q.all_of(components=[Position, Graphic], relations=[("IsIn", camera.z)]):
        pos = entity.components[Position]
        if not is_visible[pos.y, pos.x]:
            continue
        ch, fg = entity.components[Graphic]
        x = pos.x - pivot_x
        y = pos.y - pivot_y
        if 0 <= x < console.width and 0 <= y < console.height:
            console.rgb[["ch", "fg"]][y, x] = ch, fg
