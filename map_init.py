"""Map generation functions."""

from __future__ import annotations

import numpy as np
from tcod.ecs import Entity, Registry

from components import MapShape, Tiles


def new_map(registry: Registry, width: int, height: int) -> Entity:
    """Initialize and return a new map."""
    new_map = registry[object()]
    new_map.components[MapShape] = MapShape(height=height, width=width)
    new_map.components[Tiles] = np.zeros(new_map.components[MapShape], dtype=np.uint8)
    new_map.components[Tiles][:] = 2
    new_map.components[Tiles][1:-1, 1:-1] = 1
    return new_map
