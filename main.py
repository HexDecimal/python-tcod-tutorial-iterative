#!/usr/bin/env python3
"""Main script."""

from __future__ import annotations

import tcod.console
import tcod.context
import tcod.event
import tcod.tileset

TITLE = "Yet Another Roguelike Tutorial"

tileset = tcod.tileset.load_tilesheet("assets/terminal8x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)


def main() -> None:
    """Main entry point."""
    console = tcod.console.Console(90, 40)
    player_x = console.width // 2
    player_y = console.height // 2

    with tcod.context.new(console=console, tileset=tileset, title=TITLE) as context:
        while True:
            console.clear()
            console.print(x=player_x, y=player_y, text="@")
            context.present(console)
            for event in tcod.event.wait():
                match event:
                    case tcod.event.Quit():
                        raise SystemExit
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                        player_y -= 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                        player_y += 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                        player_x -= 1
                    case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                        player_x += 1


if __name__ == "__main__":
    main()
