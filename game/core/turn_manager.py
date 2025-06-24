# game/core/turn_manager.py

from enum import Enum, auto
from typing import List, Tuple
from ..interfaces import ICrewMember, IAlien
from .ship_map import ShipMap
from ..interfaces import IActor


class TurnPhase(Enum):
    PLANNING = auto()
    RESOLUTION = auto()


class TurnManager:
    def __init__(self, crew: List[ICrewMember], alien: IAlien):
        self.crew = crew
        self.alien = alien
        self.phase = TurnPhase.PLANNING
        self.movement_queue: List[Tuple[IActor, Tuple[int, int]]] = []

    def start_turn(self) -> None:
        self.phase = TurnPhase.PLANNING
        self.movement_queue.clear()

    def plan_movement(self, actor: IActor, target_coords: Tuple[int, int]) -> None:
        self.movement_queue.append((actor, target_coords))

    def resolve_movements(self, ship_map: ShipMap) -> None:
        self.phase = TurnPhase.RESOLUTION
        for actor, (x, y) in self.movement_queue:
            room = ship_map.get_room_by_coordinates(x, y)
            if not room:
                print(f"Invalid coordinates ({x}, {y}) for actor {actor.name}.")
                continue
            print(f"{actor.name} is moving to {room.name} at ({x}, {y}).")
            if room:
                actor.move_to(room)
        self.phase = TurnPhase.PLANNING
