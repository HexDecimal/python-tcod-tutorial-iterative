"""Library of actions and actor abilities."""

from __future__ import annotations

import attrs
from tcod.ecs import Entity

import map_logic
import tiles
from components import MapShape, Position, Tiles


@attrs.define
class Move:
    """Move in direction."""

    dx: int
    dy: int

    def __call__(self, actor: Entity) -> bool:
        """Verify and perform the movement on `actor`."""
        new_pos = actor.components[Position] + (self.dx, self.dy)
        height, width = new_pos.z.components[MapShape]
        if not (0 <= new_pos.x < width and 0 <= new_pos.y < height):
            return False  # Out-of-bounds
        if tiles.TILE_DATA["move_cost"][new_pos.z.components[Tiles][new_pos.y, new_pos.x]] <= 0:
            return False  # Blocked by wall
        if actor.registry.Q.all_of(tags=[new_pos, "Blocking"]):
            return False
        actor.components[Position] = new_pos
        if "IsPlayer" in actor.tags:
            map_logic.update_fov(actor)
        return True
