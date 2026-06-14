"""Library of common entity components."""

from __future__ import annotations

from typing import Final, NamedTuple, Self

import attrs
import numpy as np
import tcod.ecs.callbacks
from numpy.typing import NDArray
from tcod.ecs import Entity


@attrs.define(frozen=True)
class Position:
    """Unique position within the world."""

    x: int
    y: int
    z: Entity

    def __add__(self, xy: tuple[int, int]) -> Self:
        """Return a new Position with the vector `xy` added to it."""
        return self.__class__(self.x + xy[0], self.y + xy[1], self.z)


class Graphic(NamedTuple):
    """Simple graphic for entities."""

    ch: int
    fg: tuple[int, int, int]


@tcod.ecs.callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
    """Mirror Position as a tag on entities."""
    if old == new:
        return
    if old is not None:
        entity.tags.remove(old)
    if new is not None:
        entity.tags.add(new)
        entity.relation_tag["IsIn"] = new.z
    else:
        del entity.relation_tag["IsIn"]


class MapShape(NamedTuple):
    """Map shape tuple."""

    height: int
    width: int


Tiles: Final = ("Tiles", NDArray[np.uint8])
"""Map tiles layer."""

Visible: Final = ("Visible", NDArray[np.bool])
"""Visible map tiles layer."""

Memory: Final = ("Memory", NDArray[np.uint8])
"""Memory of map tiles."""
