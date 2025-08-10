from typing import Callable, Optional
from .base_action import BaseAction
from ...interfaces import ICrewMember, IRoom, IShipMap, ITurnManager
from ...utils.logger import log_error

class MoveAction(BaseAction):
    def __init__(self, plan_movement_callback: Callable):
        super().__init__("Move")

    def perform(self, actor: ICrewMember, **kwargs) -> None:
        get_input: Optional[Callable[[str], str]] = kwargs.get("get_input")
        turn_manager: Optional[ITurnManager] = kwargs.get("turn_manager")
        game_map: Optional[IShipMap] = kwargs.get("game_map")

        if not get_input:
            log_error("MoveAction requires get_input function in kwargs.")
            return
        if not turn_manager or not game_map:
            log_error("MoveAction requires turn_manager and game_map in kwargs.")
            return

        while turn_manager.get_remaining_actions(actor) >= self.cost:
            last_coords = (
                turn_manager.movement_queue[actor][-1]
                if turn_manager.movement_queue.get(actor)
                else actor.room.coordinates
            )
            current_room = game_map.get_room_by_coordinates(*last_coords)

            if not current_room:
                log_error(f"could not find room at coordinates {last_coords}. Check map integrity.")
                return

            print(f"\n{actor.name} is in {current_room.name} ({current_room.x}, {current_room.y})")
            neighbors = current_room.connections
            self._print_neighbor_rooms(neighbors)

            choice = get_input("Your choice: ")
            if choice.strip() == "0":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(neighbors):
                    target_room = neighbors[idx]
                    turn_manager.plan_movement(actor, (target_room.x, target_room.y))
                    turn_manager.spend_actions(actor, self.cost)
                    print(f"Planned movement for {actor.name} to {target_room.name} ({target_room.x}, {target_room.y})")
                else:
                    log_error("Invalid selection.")
            except ValueError:
                log_error("Invalid input.")

    @staticmethod
    def _print_neighbor_rooms(neighbors: list[IRoom]) -> None:
        print("Choose a connected room to move into:")
        for idx, room in enumerate(neighbors):
            print(f"{idx + 1}. {room.name} ({room.x}, {room.y})")
        print("0. Stop moving and return to action menu")
