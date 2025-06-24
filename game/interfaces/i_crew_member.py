from abc import ABC, abstractmethod
from .i_actor import IActor
from ..enums import SkillType

class ICrewMember(IActor, ABC):
    @property
    @abstractmethod
    def skills(self) -> list[SkillType]:
        pass

    @abstractmethod
    def take_damage(self, amount: int) -> None:
        pass
