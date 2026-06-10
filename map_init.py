"""Map generation functions."""

from __future__ import annotations

from random import Random

import attrs
import numpy as np
import tcod.los
import tcod.path
from tcod.ecs import Entity, Registry

from components import Graphic, MapShape, Position, Tiles


@attrs.define
class Rect:
    """Generic rectangle for defining rooms."""

    x: int
    y: int
    width: int
    height: int

    @property
    def center_x(self) -> int:
        """Return the center X coordinate of this rect."""
        return self.x + self.width // 2

    @property
    def center_y(self) -> int:
        """Return the center Y coordinate of this rect."""
        return self.y + self.height // 2

    @property
    def inner_ij(self) -> tuple[slice, slice]:
        """Return the inner area (floor) of this rect as a 2D ij array slice."""
        return slice(self.y + 1, self.y + self.height - 1), slice(self.x + 1, self.x + self.width - 1)

    @property
    def outer_ij(self) -> tuple[slice, slice]:
        """Return the outer area (including walls) of this rect as a 2D ij array slice."""
        return slice(self.y, self.y + self.height), slice(self.x, self.x + self.width)

    @property
    def right(self) -> int:
        """Return the right end of this rect."""
        return self.x + self.width

    @property
    def bottom(self) -> int:
        """Return the bottom end of this rect."""
        return self.y + self.height

    def within(self, other: Rect) -> bool:
        """Return True if `self` is within `other`."""
        return other.x <= self.x and other.y <= self.y and self.right <= other.right and self.bottom <= other.bottom

    def distance(self, other: Rect) -> int:
        """Return the distance between `self` and `other`."""
        return abs(self.center_x - other.center_x) + abs(self.center_y - other.center_y)


def new_map(registry: Registry, width: int, height: int) -> Entity:
    """Initialize and return a new map."""
    new_map = registry[object()]
    new_map.components[MapShape] = MapShape(height=height, width=width)
    new_map.components[Tiles] = np.zeros(new_map.components[MapShape], dtype=np.uint8)
    new_map.components[Tiles][:] = 2
    new_map.components[Tiles][1:-1, 1:-1] = 1
    return new_map


def connect_rooms(map_: Entity, room_1: Rect, room_2: Rect) -> None:
    """Connect rooms together."""
    costs = np.zeros(map_.components[MapShape], dtype=int)
    costs[:] = 10

    bias = np.zeros(map_.components[MapShape], dtype=bool)
    bias[room_1.center_y, :] = True
    bias[:, room_1.center_x] = True
    bias[room_2.center_y, :] = True
    bias[:, room_2.center_x] = True
    costs[bias] = 3

    costs[map_.components[Tiles] == 1] = 2
    costs[room_1.inner_ij] = 1
    costs[room_2.inner_ij] = 1
    path = tcod.path.path2d(
        costs,
        start_points=[(room_1.center_y, room_1.center_x)],
        end_points=[(room_2.center_y, room_2.center_x)],
        cardinal=1,
        diagonal=0,
    )
    map_.components[Tiles][tuple(path.T)] = 1


def generate_dungeon(registry: Registry, width: int, height: int) -> Entity:
    """Generate and return a dungeon level."""
    rng = registry[None].components[Random]
    new_map = registry[object()]
    new_map.components[MapShape] = MapShape(height=height, width=width)
    new_map.components[Tiles] = np.zeros(new_map.components[MapShape], dtype=np.uint8)

    map_rect = Rect(x=0, y=0, width=width, height=height)

    room_1 = Rect(x=width // 2 - 4, y=height // 2 - 4, width=8, height=8)
    new_map.components[Tiles][room_1.inner_ij] = 1

    rooms = [room_1]
    max_iterations = 10_000
    max_rooms = 25

    while len(rooms) < max_rooms and max_iterations > 0:
        max_iterations -= 1
        new_width, new_height = (rng.randint(6, 10), rng.randint(6, 10))

        for x, y in tcod.los.bresenham((0, 0), (rng.randint(-50, 50), rng.randint(-50, 50))).tolist():
            new_x = rooms[-1].center_x + x
            new_y = rooms[-1].center_y + y

            new_room = Rect(x=new_x - new_width // 2, y=new_y - new_height // 2, width=new_width, height=new_height)
            if not new_room.within(map_rect):
                break
            if (new_map.components[Tiles][new_room.outer_ij] != 0).any():
                continue

            new_map.components[Tiles][new_room.inner_ij] = 1
            nearest_room = min(rooms, key=new_room.distance)

            connect_rooms(new_map, new_room, nearest_room)

            rooms.append(new_room)
            break

    for random_room in rng.sample(rooms[:-1], 5):
        connect_rooms(new_map, rooms[-1], random_room)

    new_map.components[Tiles][new_map.components[Tiles] == 0] = 2

    up_stairs = registry[object()]
    up_stairs.components[Position] = Position(rooms[0].center_x, rooms[0].center_y, new_map)
    up_stairs.components[Graphic] = Graphic(ord("<"), (255, 255, 255))
    up_stairs.tags.add("StartPoint")

    down_stairs = registry[object()]
    down_stairs.components[Position] = Position(rooms[-1].center_x, rooms[-1].center_y, new_map)
    down_stairs.components[Graphic] = Graphic(ord(">"), (255, 255, 255))

    return new_map
