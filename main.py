#!/usr/bin/env python3
"""Main script."""

from __future__ import annotations

import tcod.console
import tcod.context
import tcod.event
import tcod.tileset
from tcod.ecs import Registry

import travel
from components import Graphic, Position

TITLE = "Yet Another Roguelike Tutorial"

tileset = tcod.tileset.load_tilesheet("assets/terminal8x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)


def main() -> None:
    """Main entry point."""
    console = tcod.console.Console(90, 40)

    world = Registry()
    level_0 = world["level_0"]
    player = world["player"]
    player.components[Graphic] = Graphic(ord("@"), (255, 255, 255))
    travel.force_move(player, Position(console.width // 2, console.height // 2, level_0))

    wall_prefab = world["wall"]
    wall_prefab.components[Graphic] = Graphic(ord("#"), (255, 255, 255))
    wall_prefab.tags.add("Blocking")

    for i in range(-5, 5):
        travel.spawn(wall_prefab, player.components[Position] + (-5, i))

    with tcod.context.new(console=console, tileset=tileset, title=TITLE) as context:
        while True:
            console.clear()
            for entity in world.Q.all_of(components=[Position, Graphic]):
                pos = entity.components[Position]
                ch, fg = entity.components[Graphic]
                console.print(x=pos.x, y=pos.y, text=chr(ch), fg=fg)

            context.present(console)
            for event in tcod.event.wait():
                match event:
                    case tcod.event.Quit():
                        raise SystemExit
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                        travel.move_by(player, dx=0, dy=-1)
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                        travel.move_by(player, dx=0, dy=1)
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                        travel.move_by(player, dx=-1, dy=0)
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                        travel.move_by(player, dx=1, dy=0)


if __name__ == "__main__":
    main()
