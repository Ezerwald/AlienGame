from typing import Optional
from ..interfaces import IAlien, IActor
from ..enums import ActorType
from .room import Room
from ..config import ALIEN_BASE_INITIATIVE

class Alien(IAlien):
    def __init__(self, start_room: Optional[Room]):
        self._room: Optional[Room] = start_room
        self._health: int = 10
        self._biomass: int = 20
        self._base_initiative: int = ALIEN_BASE_INITIATIVE
        self._initiative_modifier: int = 0
        self._actor_type: ActorType = ActorType.ALIEN

    @property
    def name(self) -> str:
        return "Alien"

    @property
    def room(self) -> Optional[Room]:
        return self._room

    @property
    def base_initiative(self) -> int:
        return self._base_initiative
    
    @property
    def initiative_modifier(self) -> int:
        return self._initiative_modifier
    
    @initiative_modifier.setter
    def initiative_modifier(self, value: int) -> None:
        self._initiative_modifier = value

    @property
    def actor_type(self) -> ActorType:
        return self._actor_type

    def move_to(self, room: Room) -> None:
        self._room = room

    def is_alive(self) -> bool:
        return self._health > 0

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

    def reset_initiative_modifier(self) -> None:
        self._initiative_modifier = 0
    