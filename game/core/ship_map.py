from typing import List, Optional
from ..interfaces import IRoom
from ..enums import RoomType

class ShipMap:
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._room_grid: List[List[Optional[IRoom]]] = [[None for _ in range(width)] for _ in range(height)]
        self.rooms: List[IRoom] = []

    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height
    
    @property
    def room_grid(self) -> List[List[Optional[IRoom]]]:
        return self._room_grid

    def add_room(self, room: IRoom) -> None:
        self.handle_duplicate_room(room)
        self.rooms.append(room)
        self.room_grid[room.x][room.y] = room

    def handle_duplicate_room(self, room: IRoom) -> None:
        count = self.get_room_count_by_type(room.room_type)
        if count >= 1:
            get_room = (self.get_room_by_type(room.room_type))[-1] if self.get_room_by_type(room.room_type) else None
            # If a room with the same name exists, rename it to avoid duplicates
            if get_room is not None:
                get_room.name = f"{room.name} {count}"
                room.name = f"{room.name} {count + 1}"

    def get_room_by_coordinates(self, x: int, y: int) -> Optional[IRoom]:
        if 0 <= y < len(self.room_grid) and 0 <= x < len(self.room_grid[0]):
            return self.room_grid[y][x]
        return None
    
    def get_room_by_name(self, name: str) -> Optional[List[IRoom]]:
        result: List[IRoom] = []
        for room in self.rooms:
            if room.name == name:
                result.append(room)
        return result if result else None
    
    def get_room_by_type(self, room_type: RoomType) -> Optional[List[IRoom]]:
        result: List[IRoom] = []
        for room in self.rooms:
            if room.room_type == room_type:
                result.append(room)
        return result if result else None

    def get_room_count_by_type(self, room_type: RoomType) -> int:
        return sum(1 for room in self.rooms if room.room_type == room_type)

    def connect_rooms(self, room1_coordinates: tuple[int, int], room2_coordinates: tuple[int, int]) -> None:
        room1: IRoom = self.get_room_by_coordinates(*room1_coordinates)
        room2: IRoom = self.get_room_by_coordinates(*room2_coordinates)
        if room1 and room2:
            room1.connect(room2)

    def connect_rooms_vents(self, room1_coordinates: tuple[int, int], room2_coordinates: tuple[int, int]) -> None:
        room1: IRoom = self.get_room_by_coordinates(*room1_coordinates)
        room2: IRoom = self.get_room_by_coordinates(*room2_coordinates)
        if room1 and room2:
            room1.connect_vent(room2)

