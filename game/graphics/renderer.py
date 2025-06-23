import pygame
from typing import List
from game.core.ship_map import ShipMap
from game.interfaces.i_actor import IActor
from game.core.alien import Alien
from game.enums.actor_type import ActorType
from game.core.room import Room
from .renderer_constants import (
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

def render_map(smap: ShipMap, crew: List[IActor], alien: Alien) -> None:
    pygame.init()
    font = pygame.font.SysFont(None, 18)

    width: int = smap.width * ROOM_SIZE + MARGIN * 2
    height: int = smap.height * ROOM_SIZE + MARGIN * 2
    screen: pygame.Surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ship Map")

    screen.fill((0, 0, 0))  # Clear screen

    # Draw rooms
    for room in smap.rooms:
        _draw_room(screen, font, room)

    # Draw crew & alien
    for actor in crew + [alien]:
        _draw_actor(screen, actor)

    pygame.display.flip()

    # Event loop stub to keep window visible for now (replace later with main game loop)
    _handle_temp_events()


def _draw_room(screen: pygame.Surface, font: pygame.font.Font, room: Room) -> None:
    x: int = room.x * ROOM_SIZE + MARGIN
    y: int = room.y * ROOM_SIZE + MARGIN
    rect = pygame.Rect(x, y, ROOM_SIZE, ROOM_SIZE)

    pygame.draw.rect(screen, ROOM_COLOR, rect, 2)

    name_text = font.render(room.name, True, TEXT_COLOR)
    screen.blit(name_text, (x + 4, y + 4))

    # Corridor connections
    for other in room.connections:
        ox: int = other.x * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
        oy: int = other.y * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
        pygame.draw.line(screen, CORRIDOR_COLOR, (x + ROOM_SIZE // 2, y + ROOM_SIZE // 2), (ox, oy), CORRIDOR_WIDTH)

    # Vent connections (if defined)
    if hasattr(room, 'vent_connections'):
        for vent in getattr(room, 'vent_connections'):
            vx: int = vent.x * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
            vy: int = vent.y * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
            pygame.draw.line(screen, VENT_COLOR, (x + ROOM_SIZE // 2, y + ROOM_SIZE // 2), (vx, vy), VENT_WIDTH)


def _draw_actor(screen: pygame.Surface, actor: IActor) -> None:
    room = actor.get_room()
    if not room:
        return
    x = room.x * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN
    y = room.y * ROOM_SIZE + ROOM_SIZE // 2 + MARGIN

    color = CREW_COLOR if actor.get_actor_type() == ActorType.CREW else ALIEN_COLOR
    pygame.draw.circle(screen, color, (x, y), 8)


def _handle_temp_events() -> None:
    # Temporary event handling so window doesn't freeze
    # Replace or expand in your main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
