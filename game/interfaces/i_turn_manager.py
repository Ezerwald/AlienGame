from abc import ABC, abstractmethod

from typing import Tuple
from ..interfaces import IActor, IRoom, IShipMap

class ITurnManager(ABC):
    @abstractmethod
    def start_turn(self) -> None:
        pass

    @abstractmethod
    def plan_movement(self, actor: IActor, target_coords: Tuple[int, int]) -> None:
        pass

    @abstractmethod
    def get_remaining_actions(self, actor: IActor) -> int:
        pass

    @abstractmethod
    def resolve_movements(self, ship_map: IShipMap) -> None:
        pass

    @abstractmethod
    def _is_conflict(self, actor: IActor, room: IRoom) -> bool:
        pass