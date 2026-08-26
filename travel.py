"""Movement and pathfinder logic."""

from __future__ import annotations

from tcod.ecs import Entity, IsA

from components import Position


def force_move(entity: Entity, dest: Position) -> None:
    """Move `entity` to `dest` and apply side-effects of movement."""
    entity.components[Position] = dest


def can_move_to(entity: Entity, dest: Position) -> bool:
    """Check and return the status of moving `entity` to `dest`."""
    world = entity.registry
    if world.Q.all_of(tags=[dest, "Blocking"]):  # noqa: SIM103
        return False  # No blocking entities at dest
    return True  # Valid move


def move_by(entity: Entity, dx: int, dy: int) -> bool:
    """Move `entity` by the relative position `dx,dy` if possible."""
    dest = entity.components[Position] + (dx, dy)
    move_result = can_move_to(entity, dest)
    if move_result:
        force_move(entity, dest)
    return move_result


def spawn(template: Entity, dest: Position) -> Entity:
    """Spawn an instance of 'template' at 'dest'."""
    world = template.registry
    instance = world[object()]  # New anonymous entity
    instance.relation_tag[IsA] = template  # Inherit components/tags/relations from template
    force_move(instance, dest)  # Assign Position with possible side-effects
    return instance
