from typing import Optional
from ..interfaces import ICrewMember
from ..enums import ActorType
from ..enums import SkillType
from .room import Room

class CrewMember(ICrewMember):
    def __init__(self, name: str, start_room: Optional[Room], skills: Optional[list[SkillType]] = None):
        self._name: str = name
        self._room: Optional[Room] = start_room
        self._health: int = 2
        self._skills: list[SkillType] = skills or []

    def get_name(self) -> str:
        return self._name

    def get_room(self) -> Optional[Room]:
        return self._room

    def move_to(self, room: Room) -> None:
        self._room = room

    def is_alive(self) -> bool:
        return self._health > 0

    def get_actor_type(self) -> ActorType:
        return ActorType.CREW

    def get_skills(self) -> list[SkillType]:
        return self._skills

    def take_damage(self, amount: int) -> None:
        self._health = max(0, self._health - amount)
