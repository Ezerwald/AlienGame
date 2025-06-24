from abc import ABC, abstractmethod
from typing import Optional
from .i_room import IRoom
from ..enums import ActorType

class IActor(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def room(self) -> Optional[IRoom]:
        pass

    @property
    @abstractmethod
    def base_initiative(self) -> int:
        pass

    @property
    @abstractmethod
    def initiative_modifier(self) -> int:
        pass

    @initiative_modifier.setter
    @abstractmethod
    def initiative_modifier(self, value: int) -> None:
        pass

    @abstractmethod
    def move_to(self, room: IRoom) -> None:
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass

    @abstractmethod
    def get_actor_type(self) -> ActorType:
        pass

    @abstractmethod
    def reset_initiative_modifier(self) -> None:    #TODO : remove this method
        pass
