from typing import List, Dict
import pygame
from pygame.locals import QUIT
from ..graphics import render_map, ROOM_SIZE, MARGIN
from ..config import ROOM_LAYOUT, VENT_LAYOUT, MAX_CREW_MEMBER_ACTIONS, MAX_ALIEN_ACTIONS
from ..utils.map_loader import create_map_from_text, create_vents_from_list
from ..utils import get_user_input
from ..interfaces import ICrewMember, IAlien, IActor
from .ship_map import ShipMap
from .crew_member import CrewMember
from .alien import Alien
from .turn_manager import TurnManager
from ..utils import show_actor_info, clear_terminal

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
            self._action_phase()
            self._movement_planning_phase()
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

    def _action_phase(self):
        clear_terminal()

        while True:
            print("\n--- ACTION PHASE ---")
            print("\nChoose a crew member to command:")

            for idx, member in enumerate(self.crew):
                remaining = self.turn_manager.get_remaining_actions(member)
                print(f"{idx + 1}. {member.name} ({remaining}/{MAX_CREW_MEMBER_ACTIONS})")
            print("0. Continue to movement planning")

            choice = get_user_input("Your choice: ")

            if choice == "0":
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.crew):
                    member = self.crew[idx]
                    remaining = self.turn_manager.get_remaining_actions(member)

                    if remaining == 0:
                        print(f"{member.name} has no remaining actions.")
                    else:
                        self._crew_action_menu(member)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")

    def _crew_action_menu(self, member: ICrewMember):
        show_actor_info(member)

        while self.turn_manager.get_remaining_actions(member) > 0:
            remaining = self.turn_manager.get_remaining_actions(member)
            print(f"\nActions remaining for {member.name} ({remaining}/{MAX_CREW_MEMBER_ACTIONS})")
            print("1. Wait")
            print("2. Do something else (placeholder)")
            print("0. Finish")

            choice = get_user_input("Choose action: ")

            if choice == "1":
                print(f"{member.name} waits.")
                self.turn_manager.log_action(member, "Wait")
            elif choice == "2":
                print(f"{member.name} does something else.")
                self.turn_manager.log_action(member, "Placeholder Action")
            elif choice == "0":
                break
            else:
                print("Unknown choice.")

    def _movement_planning_phase(self):
        while True:
            print("\n--- MOVEMENT PLANNING PHASE ---")
            print("\nChoose a crew member to plan movement:")
            for idx, actor in enumerate(self.crew):  # Exclude alien
                remaining = self.turn_manager.get_remaining_actions(actor)
                print(f"{idx + 1}. {actor.name} ({remaining}/{MAX_CREW_MEMBER_ACTIONS})")
            print("0. Continue to resolution phase")

            choice = get_user_input("Your choice: ")

            if choice == "0":
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.crew):
                    actor = self.crew[idx]
                    remaining = self.turn_manager.get_remaining_actions(actor)
                    if remaining == 0:
                        print(f"{actor.name} has no movement actions left.")
                    else:
                        for _ in range(remaining):
                            self._plan_movement_for_actor(actor)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")


    def _plan_movement_for_actor(self, actor: IActor):
        show_actor_info(actor)

        last_coords = (
            self.turn_manager.movement_queue[actor][-1]
            if self.turn_manager.movement_queue.get(actor)
            else actor.room.coordinates
        )

        current_room = self.map.get_room_by_coordinates(*last_coords)
        
        print(f"Current destination room: {current_room.name}")

        if not current_room:
            print(f"Error: could not find room at {last_coords}.")
            return

        neighbors = current_room.connections

        print(f"\nMovement options for {actor.name}:")
        for idx, room in enumerate(neighbors):
            print(f"{idx + 1}. {room.name} ({room.x}, {room.y})")
        print("0. Skip movement")

        choice = get_user_input("Choose room: ")
        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(neighbors):
                room = neighbors[idx]
                self.turn_manager.plan_movement(actor, (room.x, room.y))
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")


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
