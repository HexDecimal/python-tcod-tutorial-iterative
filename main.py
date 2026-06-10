#!/usr/bin/env python3
"""Main script."""

from __future__ import annotations

from random import Random

import tcod.console
import tcod.context
import tcod.event
import tcod.tileset
from tcod.ecs import Registry

import actions
import map_init
import rendering
from components import Graphic, Position

TITLE = "Yet Another Roguelike Tutorial"

tileset = tcod.tileset.load_tilesheet("assets/terminal8x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)


def main() -> None:
    """Main entry point."""
    console = tcod.console.Console(90, 40)

    world = Registry()
    world[None].components[Random] = Random()
    level_0 = map_init.generate_dungeon(world, width=100, height=50)
    player = world["player"]
    (start,) = world.Q.all_of(tags=["StartPoint"], relations=[("IsIn", level_0)])
    player.components[Position] = start.components[Position]
    player.components[Graphic] = Graphic(ord("@"), (255, 255, 255))

    with tcod.context.new(console=console, tileset=tileset, title=TITLE) as context:
        while True:
            console.clear()
            rendering.render_map(console, player.components[Position])

            context.present(console)
            for event in tcod.event.wait():
                match event:
                    case tcod.event.Quit():
                        raise SystemExit
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                        actions.Move(dx=0, dy=-1)(player)
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                        actions.Move(dx=0, dy=1)(player)
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                        actions.Move(dx=-1, dy=0)(player)
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                        actions.Move(dx=1, dy=0)(player)


if __name__ == "__main__":
    main()
