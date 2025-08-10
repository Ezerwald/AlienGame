from typing import List, Dict
import pygame
from pygame.locals import QUIT

from ..utils import log_error
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
from ..interfaces import IAction, IShipMap, ITurnManager
from .crew_actions import MoveAction, FixAction, PeekAction, AttackAction


class GameManager:
    def __init__(self):
        self.map: IShipMap = self._create_map()
        self.crew: List[ICrewMember] = self._create_crew()
        self.alien: IAlien = Alien(self.map.get_room_by_coordinates(2, 2))
        self.turn_manager: ITurnManager = TurnManager(self.crew, self.alien)

        # Available actions of crew member for Action Phase
        self.crew_available_actions: List[IAction] = [
            MoveAction(self.turn_manager.plan_movement),  # passes movement callback
            FixAction(),
            PeekAction(),
            AttackAction()
        ]

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

            print("0. End Action Phase")

            choice = get_user_input("Your choice: ")

            if choice == "0":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.crew):
                    actor = self.crew[idx]
                    self._actor_action_menu(actor)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")

    def _actor_action_menu(self, actor: IActor):
        while True:
            clear_terminal()
            remaining = self.turn_manager.get_remaining_actions(actor)
            show_actor_info(actor)

            print(f"\nActions remaining for {actor.name} ({remaining}/{MAX_CREW_MEMBER_ACTIONS})")

            current_room = actor.room
            possible_actions = [
                action for action in self.crew_available_actions
                if action.is_available(actor, current_room)
            ]

            # Show actions regardless of AP, but flag unavailable ones
            for idx, action in enumerate(possible_actions, 1):
                status = f"(cost: {action.cost})" if remaining >= action.cost else "(Unavailable)"
                print(f"{idx}. {action.name} {status}")

            print("0. Back to crew selection")

            choice = get_user_input("Choose action: ")

            if choice == "0":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(possible_actions):
                    action = possible_actions[idx]

                    if remaining < action.cost:
                        print(f"{actor.name} has no actions left to perform {action.name}.")
                        get_user_input("Press Enter to continue...")
                        continue

                    # Execute action — AP deduction happens inside action itself
                    action.perform(
                        actor,
                        get_input=get_user_input,
                        turn_manager=self.turn_manager,
                        game_map=self.map,
                        alien=self.alien
                    )

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
