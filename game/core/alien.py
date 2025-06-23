from typing import Optional
from ..interfaces import IAlien, IActor
from ..enums import ActorType
from .room import Room

class Alien(IAlien):
    def __init__(self, start_room: Optional[Room]):
        self._room: Optional[Room] = start_room
        self._health: int = 10
        self._biomass: int = 20

    def get_name(self) -> str:
        return "Alien"

    def get_room(self) -> Optional[Room]:
        return self._room

    def move_to(self, room: Room) -> None:
        self._room = room

    def is_alive(self) -> bool:
        return self._health > 0

    def get_actor_type(self) -> ActorType:
        return ActorType.ALIEN

    def use_biomass(self, amount: int) -> None:
        if amount > self._biomass:
            raise ValueError("Not enough biomass!")
        self._biomass -= amount

    def add_biomass(self, amount: int) -> None:
        self._biomass += amount

    @property
    def biomass(self) -> int:
        return self._biomass


    def attack(self, target: IActor) -> None:
        if hasattr(target, 'take_damage'):
            target.take_damage(2)  # TODO: Improve damage calculation

    