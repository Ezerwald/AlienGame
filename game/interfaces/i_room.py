from abc import ABC, abstractmethod
from ..enums import RoomType
from typing import List, Tuple


class IRoom(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def x(self) -> int:
        ...

    @property
    @abstractmethod
    def y(self) -> int:
        ...

    @property
    @abstractmethod
    def coordinates(self) -> Tuple[int, int]:
        ...

    @property
    @abstractmethod
    def room_type(self) -> RoomType:
        ...

    @abstractmethod
    def connect(self, other: "IRoom") -> None:
        ...

    @abstractmethod
    def connect_vent(self, other: "IRoom") -> None:
        ...

    @property
    @abstractmethod
    def connections(self) -> List["IRoom"]:
        ...

    @property
    @abstractmethod
    def vent_connections(self) -> List["IRoom"]:
        ...

    @property
    @abstractmethod
    def has_vent(self) -> bool:
        ...
