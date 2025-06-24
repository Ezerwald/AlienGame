from typing import List
from .ship_map import ShipMap
from .room import Room
from ..enums import RoomType
from .crew_member import CrewMember
from .alien import Alien
from ..graphics import render_map
from ..interfaces import ICrewMember, IAlien
from ..utils.map_loader import create_map_from_text, create_vents_from_list
import pygame
from pygame.locals import QUIT
from ..config import ROOM_SIZE, MARGIN, ROOM_LAYOUT, VENT_LAYOUT


class GameManager:
    def __init__(self):
        self.map: ShipMap = self._create_map()
        self.crew: List[ICrewMember] = [
            CrewMember("Alice", self.map.get_room_by_coordinates(0, 0)),
            CrewMember("Bob", self.map.get_room_by_coordinates(1, 0)),
            CrewMember("Charlie", self.map.get_room_by_coordinates(0, 1)),
        ]
        self.alien: IAlien = Alien(self.map.get_room_by_coordinates(2, 2))

    def _create_map(self) -> ShipMap:

        smap = create_map_from_text(ROOM_LAYOUT)
        create_vents_from_list(smap, VENT_LAYOUT)

        return smap

    def run(self) -> None:
        pygame.init()
        width = self.map.width * ROOM_SIZE + MARGIN * 2
        height = self.map.height * ROOM_SIZE + MARGIN * 2
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Alien Game")
        font = pygame.font.SysFont(None, 18)

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            render_map(screen, font, self.map, self.crew, self.alien)
            clock.tick(30)

        pygame.quit()
