#!/usr/bin/env python3
"""Main script."""

from __future__ import annotations

import tcod.console
import tcod.context
import tcod.event
import tcod.tileset

tileset = tcod.tileset.load_tilesheet("assets/terminal8x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)


def main() -> None:
    """Main entry point."""
    console = tcod.console.Console(90, 40)

    with tcod.context.new(console=console, tileset=tileset) as context:
        while True:
            console.clear()
            console.print(x=0, y=0, text="Hello World")
            context.present(console)
            for event in tcod.event.wait():
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit


if __name__ == "__main__":
    main()
