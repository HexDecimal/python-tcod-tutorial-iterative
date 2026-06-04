"""Library of actions and actor abilities."""

from __future__ import annotations

import attrs
from tcod.ecs import Entity

from components import Position


@attrs.define
class Move:
    """Move in direction."""

    dx: int
    dy: int

    def __call__(self, actor: Entity) -> bool:
        """Verify and perform the movement on `actor`."""
        new_pos = actor.components[Position] + (self.dx, self.dy)
        if actor.registry.Q.all_of(tags=[new_pos]):
            return False
        actor.components[Position] = new_pos
        return True
