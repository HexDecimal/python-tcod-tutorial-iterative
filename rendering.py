"""Common rendering functions."""

from __future__ import annotations

import tcod.camera
import tcod.console

import tiles
from components import Graphic, MapShape, Position, Tiles


def render_map(console: tcod.console.Console, camera: Position) -> None:
    """Render the map at `camera` to the `console`."""
    world = camera.z.registry
    pivot_x, pivot_y = camera.x - console.width // 2, camera.y - console.height // 2

    screen_slice, world_slice = tcod.camera.get_slices(
        screen=(console.height, console.width), world=camera.z.components[MapShape], camera=(pivot_y, pivot_x)
    )

    world_tiles = camera.z.components[Tiles][world_slice]
    console.rgb[screen_slice] = tiles.TILE_DATA[["ch", "fg", "bg"]][world_tiles]

    for entity in world.Q.all_of(components=[Position, Graphic]):
        pos = entity.components[Position]
        ch, fg = entity.components[Graphic]
        x = pos.x - pivot_x
        y = pos.y - pivot_y
        if 0 <= x < console.width and 0 <= y < console.height:
            console.rgb[["ch", "fg"]][y, x] = ch, fg
