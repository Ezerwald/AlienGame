from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from ..interfaces import IRoom
from ..enums import RoomType

class IShipMap(ABC):
    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass

    @property
    @abstractmethod
    def room_grid(self) -> List[List[Optional[IRoom]]]:
        pass

    @property
    @abstractmethod
    def rooms(self) -> List[IRoom]:
        pass

    @abstractmethod
    def add_room(self, room: IRoom) -> None:
        pass

    @abstractmethod
    def handle_duplicate_room(self, room: IRoom) -> None:
        pass

    @abstractmethod
    def get_room_by_coordinates(self, x: int, y: int) -> Optional[IRoom]:
        pass

    @abstractmethod
    def get_room_by_name(self, name: str) -> Optional[List[IRoom]]:
        pass

    @abstractmethod
    def get_room_by_type(self, room_type: RoomType) -> Optional[List[IRoom]]:
        pass

    @abstractmethod
    def get_room_count_by_type(self, room_type: RoomType) -> int:
        pass

    @abstractmethod
    def connect_rooms(self, room1_coordinates: Tuple[int, int], room2_coordinates: Tuple[int, int]) -> None:
        pass

    @abstractmethod
    def connect_rooms_vents(self, room1_coordinates: Tuple[int, int], room2_coordinates: Tuple[int, int]) -> None:
        pass
