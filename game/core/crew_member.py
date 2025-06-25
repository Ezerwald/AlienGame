from typing import Optional
from ..interfaces import ICrewMember
from ..enums import ActorType
from ..enums import SkillType
from ..config import CREW_MEMBER_BASE_INITIATIVE
from ..interfaces import IRoom

class CrewMember(ICrewMember):
    def __init__(self, name: str, start_room: Optional[IRoom], skills: Optional[list[SkillType]] = None):
        self._name: str = name
        self._room: Optional[IRoom] = start_room
        self._health: int = 2
        self._skills: list[SkillType] = skills or []
        self._base_initiative: int = CREW_MEMBER_BASE_INITIATIVE
        self._initiative_modifier: int = 0
        self._actor_type: ActorType = ActorType.CREW

    @property
    def name(self) -> str:
        return self._name

    @property
    def room(self) -> Optional[IRoom]:
        return self._room
    
    @property
    def skills(self) -> list[SkillType]:
        return self._skills

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

    def move_to(self, room: IRoom) -> None:
        self._room = room

    def is_alive(self) -> bool:
        return self._health > 0
    
    def take_damage(self, amount: int) -> None:
        self._health = max(0, self._health - amount)

    def heal(self, amount: int) -> None:
        self._health += amount
        if self._health > 2:
            self._health = 2

    def reset_initiative_modifier(self) -> None:
        self._initiative_modifier = 0