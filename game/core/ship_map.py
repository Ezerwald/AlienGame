from typing import List, Optional
from ..interfaces import IRoom

class ShipMap:
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self.grid: List[List[Optional[IRoom]]] = [[None for _ in range(width)] for _ in range(height)]
        self.rooms: List[IRoom] = []

    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height

    def add_room(self, room: IRoom) -> None:
        self.rooms.append(room)
        self.grid[room.coordinates[0]][room.coordinates[1]] = room

    def get_room(self, x: int, y: int) -> Optional[IRoom]:
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x]
        return None
    
    def connect_rooms(self, room1_coordinates: tuple[int, int], room2_coordinates: tuple[int, int]) -> None:
        room1: IRoom = self.get_room(*room1_coordinates)
        room2: IRoom = self.get_room(*room2_coordinates)
        if room1 and room2:
            room1.connect(room2)

    def connect_rooms_vents(self, room1_coordinates: tuple[int, int], room2_coordinates: tuple[int, int]) -> None:
        room1: IRoom = self.get_room(*room1_coordinates)
        room2: IRoom = self.get_room(*room2_coordinates)
        if room1 and room2:
            room1.connect_vent(room2)

