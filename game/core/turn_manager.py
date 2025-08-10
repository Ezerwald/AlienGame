from enum import Enum, auto
from typing import List, Tuple, Dict
from ..interfaces import ICrewMember, IAlien, IActor
from .ship_map import ShipMap
from ..config import MAX_CREW_MEMBER_ACTIONS, MAX_ALIEN_ACTIONS
from ..enums import ActorType
from ..interfaces import IRoom, IShipMap


class TurnPhase(Enum):
    ACTION = auto()
    PLANNING = auto()
    RESOLUTION = auto()


class TurnManager:
    def __init__(self, crew: List[ICrewMember], alien: IAlien):
        self.crew = crew
        self.alien = alien
        self.phase = TurnPhase.ACTION
        self.movement_queue: Dict[IActor, List[Tuple[int, int]]] = {}
        self.remaining_actions: Dict[str, int] = {}
        self.action_log: List[str] = []

    def start_turn(self) -> None:
        self.phase = TurnPhase.ACTION
        self.action_log.clear()
        self.remaining_actions = {
            actor.name: MAX_CREW_MEMBER_ACTIONS if actor.actor_type == ActorType.CREW else MAX_ALIEN_ACTIONS
            for actor in self.crew + [self.alien]
        }
        self.movement_queue.clear()

    def log_action(self, actor: IActor, description: str) -> None:
        print(f"{actor.name} action: {description}")
        self.action_log.append(f"{actor.name}: {description}")
        self.remaining_actions[actor.name] = max(0, self.remaining_actions[actor.name] - 1)

    def plan_movement(self, actor: IActor, target_coords: Tuple[int, int]) -> None:
        if self.remaining_actions.get(actor.name, 0) > 0:
            self.movement_queue.setdefault(actor, []).append(target_coords)
        else:
            print(f"{actor.name} has no remaining movement actions.")

    def get_remaining_actions(self, actor: IActor) -> int:
        return self.remaining_actions.get(actor.name, 0)
    
    def spend_actions(self, actor: IActor, cost: int) -> None:
        self.remaining_actions[actor.name] = max(0, self.remaining_actions.get(actor.name, 0) - cost)

    def resolve_movements(self, ship_map: IShipMap) -> None:
        self.phase = TurnPhase.RESOLUTION
        print("\nResolving movements...")
        step = 0
        actors = list(self.movement_queue.keys())

        while True:
            moved_this_round = False
            for actor in actors:
                if actor not in self.movement_queue or not self.movement_queue[actor]:
                    continue

                planned = self.movement_queue.get(actor, [])
                if step < len(planned):
                    x, y = planned[step]
                    room = ship_map.get_room_by_coordinates(x, y)
                    if room:
                        actor.move_to(room)
                        print(f"{actor.name} moves to {room.name} ({x}, {y})")
                        moved_this_round = True

                        # Stop movement if there's an enemy in the room
                        if self._is_conflict(actor, room):
                            continue
            if not moved_this_round:
                break
            step += 1

    def _is_conflict(self, actor: IActor, room: IRoom) -> bool:
        for other in self.crew + [self.alien]:
            if other is actor:
                continue
            # Only interrupt if enemy is in the same room
            if (
                other.actor_type != actor.actor_type and
                other.room == room
            ):
                # Cancel further movements for both actors
                self.movement_queue[actor] = []
                self.movement_queue[other] = []

                print(f"{actor.name} and {other.name} encounter each other in {room.name}. Both stop moving.")

                return True
        return False
