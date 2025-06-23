from typing import List, Tuple
from ..interfaces import IRoom
from ..enums import RoomType 

class Room(IRoom):
    def __init__(self, name: str, x: int, y: int, room_type: RoomType = RoomType.GENERIC):
        self._name: str = name
        self._x: int = x
        self._y: int = y
        self._room_type: RoomType = room_type
        self._connections: List[IRoom] = []
        self._vent_connections: List[IRoom] = []
        self._has_vent: bool = False
        self.broken: bool = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y


    @property
    def coordinates(self) -> Tuple[int, int]:
        return (self._x, self._y)

    @property
    def room_type(self) -> RoomType:
        return self._room_type

    @property
    def connections(self) -> List[IRoom]:
        return self._connections

    @property
    def vent_connections(self) -> List[IRoom]:
        return self._vent_connections

    @property
    def has_vent(self) -> bool:
        return self._has_vent

    def connect(self, other: IRoom) -> None:
        if other not in self._connections:
            self._connections.append(other) # TODO: Add connection status change
            other.connect(self)

    def connect_vent(self, other: IRoom) -> None:
        self._has_vent = True
        other._has_vent = True
        if other not in self._vent_connections:
            self._vent_connections.append(other)
            other.connect_vent(self)
