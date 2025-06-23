from abc import ABC, abstractmethod
from typing import Optional
from .i_room import IRoom
from ..enums import ActorType

class IActor(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_room(self) -> Optional[IRoom]:
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
