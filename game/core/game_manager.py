from typing import List, Dict
import pygame
from pygame.locals import QUIT
from ..graphics import render_map, ROOM_SIZE, MARGIN
from ..config import ROOM_LAYOUT, VENT_LAYOUT
from ..utils.map_loader import create_map_from_text, create_vents_from_list
from ..utils import get_user_input
from ..ui import PlanningUIManager
from ..interfaces import ICrewMember, IAlien, IActor
from .ship_map import ShipMap
from .crew_member import CrewMember
from .alien import Alien
from .turn_manager import TurnManager
from ..enums import ActorType

class GameManager:
    def __init__(self):
        self.map: ShipMap = self._create_map()
        self.crew: List[ICrewMember] = self._create_crew()
        self.alien: IAlien = Alien(self.map.get_room_by_coordinates(2, 2))
        self.turn_manager = TurnManager(self.crew, self.alien)

    def _create_map(self) -> ShipMap:
        smap = create_map_from_text(ROOM_LAYOUT)
        create_vents_from_list(smap, VENT_LAYOUT)
        return smap

    def _create_crew(self) -> List[ICrewMember]:
        return [
            CrewMember("Alice", self.map.get_room_by_coordinates(0, 0)),
            CrewMember("Bob", self.map.get_room_by_coordinates(1, 0)),
            CrewMember("Charlie", self.map.get_room_by_coordinates(0, 1)),
        ]

    def run(self) -> None:
        self._init_pygame()
        screen, font, clock = self._create_window()

        running = True
        while running:
            running = self._handle_pygame_events()
            render_map(screen, font, self.map, self.crew, self.alien)

            self._start_turn()
            self._planning_phase()
            self._resolution_phase(screen, font)

            get_user_input("\n[Press Enter to continue to next turn]")
            clock.tick(30)

        pygame.quit()

    def _init_pygame(self) -> None:
        pygame.init()

    def _create_window(self):
        width = self.map.width * ROOM_SIZE + MARGIN * 2
        height = self.map.height * ROOM_SIZE + MARGIN * 2
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Alien Game")
        font = pygame.font.Font(None, 14)
        clock = pygame.time.Clock()
        return screen, font, clock

    def _handle_pygame_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        return True

    def _start_turn(self) -> None:
        self.turn_manager.start_turn()
        print("\n--- PLANNING PHASE ---")

    def _planning_phase(self) -> None:
        actors_by_initiative: Dict[int, List[IActor]] = self._group_actors_by_initiative()

        for initiative in sorted(actors_by_initiative.keys()):
            group = actors_by_initiative[initiative]
            print(f"\n== Initiative {initiative} ==")

            crew_group = [a for a in group if a.get_actor_type() == ActorType.CREW]
            if crew_group:
                ui = PlanningUIManager(crew_group)
                ui.run(self.turn_manager.plan_movement)

            alien_group = [a for a in group if a.get_actor_type() == ActorType.ALIEN]
            for alien in alien_group:
                print(f"{alien.name} is planning actions... (to be implemented)")

        for actor in self.crew + [self.alien]:
            actor.reset_initiative_modifier()

    def _group_actors_by_initiative(self) -> Dict[int, List[IActor]]:
        all_actors = [a for a in self.crew if a.is_alive()] + [self.alien]
        initiative_groups: Dict[int, List[IActor]] = {}

        for actor in all_actors:
            total = actor.base_initiative + actor.initiative_modifier
            initiative_groups.setdefault(total, []).append(actor)

        return initiative_groups

    def _resolution_phase(self, screen, font) -> None:
        print("\n--- RESOLUTION PHASE ---")
        self.turn_manager.resolve_movements(self.map)
        render_map(screen, font, self.map, self.crew, self.alien)
