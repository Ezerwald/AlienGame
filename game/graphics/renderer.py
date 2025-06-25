import pygame
from typing import List
from game.core.ship_map import ShipMap
from game.interfaces.i_actor import IActor
from game.core.alien import Alien
from game.enums.actor_type import ActorType
from game.core.room import Room
from .renderer_config import (
    ROOM_SIZE,
    MARGIN,
    CORRIDOR_WIDTH,
    VENT_WIDTH,
    ROOM_COLOR,
    TEXT_COLOR,
    CORRIDOR_COLOR,
    VENT_COLOR,
    CREW_COLOR,
    ALIEN_COLOR
)

x = ROOM_SIZE // 5
# Offsets for actor rendering to avoid overlap
actor_offsets = [(-x, -x), (-x, x), (x, x), (x, -x)]
actor_collors = []

def render_map(screen: pygame.Surface, font: pygame.font.Font, smap: ShipMap, crew: List[IActor], alien: Alien) -> None:
    screen.fill((0, 0, 0))  # Clear screen

    for room in smap.rooms:
        _draw_room(screen, font, room)

    for i, actor in enumerate(crew + [alien]):
        _draw_actor(screen, actor, i, font)

    pygame.display.flip()


def _draw_room(screen: pygame.Surface, font: pygame.font.Font, room: Room) -> None:
    _draw_room_box_and_label(screen, font, room)
    #_draw_corridor_connections(screen, room)
    _draw_vent_connections(screen, room)


def _draw_room_box_and_label(screen: pygame.Surface, font: pygame.font.Font, room: Room) -> None:
    x: int = room.x * ROOM_SIZE + MARGIN
    y: int = room.y * ROOM_SIZE + MARGIN
    rect = pygame.Rect(x, y, ROOM_SIZE, ROOM_SIZE)

    pygame.draw.rect(screen, ROOM_COLOR, rect, 2)
    name_text = font.render(f"{room.name} ({room.x}, {room.y})", True, TEXT_COLOR)
    screen.blit(name_text, (x + 4, y + 4))


def _draw_corridor_connections(screen: pygame.Surface, room: Room) -> None:
    x_center = room.x * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
    y_center = room.y * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN

    for other in room.connections:
        ox = other.x * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
        oy = other.y * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
        pygame.draw.line(screen, CORRIDOR_COLOR, (x_center, y_center), (ox, oy), CORRIDOR_WIDTH)


def _draw_vent_connections(screen: pygame.Surface, room: Room) -> None:
    x_center = room.x * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
    y_center = room.y * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN

    for vent in getattr(room, 'vent_connections', []):
        vx = vent.x * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
        vy = vent.y * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
        pygame.draw.line(screen, VENT_COLOR, (x_center, y_center), (vx, vy), VENT_WIDTH)


def _draw_actor(screen: pygame.Surface, actor: IActor, i: int, font) -> None:
    room = actor.room
    if not room:
        return
    x = room.x * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN + actor_offsets[i][0]
    y = room.y * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN + actor_offsets[i][1]
    color = CREW_COLOR if actor.actor_type == ActorType.CREW else ALIEN_COLOR
    name_text = font.render(actor.name, True, color)
    screen.blit(name_text, (x-10, y - 20))
    pygame.draw.circle(screen, color, (x, y), 8)
