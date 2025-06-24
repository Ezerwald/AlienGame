from typing import List, Dict
from ..core.ship_map import ShipMap
from ..core.room import Room
from ..enums.room_type import RoomType
from collections import defaultdict
from typing import List, Optional
from ..interfaces import IRoom
from .map_loader_config import ROOM_TYPE_MAPPING

def create_map_from_text(layout: List[str]) -> ShipMap:
    height = len(layout)
    width = max(len(row) for row in layout)
    ship_map = ShipMap(width, height)

    room_grid: List[List[Optional[IRoom]]] = [[None for _ in range(width)] for _ in range(height)]

    # Create room instances
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if char == "0":
                continue
            if char not in ROOM_TYPE_MAPPING:
                raise ValueError(f"Invalid room type symbol: '{char}' at ({x}, {y})")
            room_type = ROOM_TYPE_MAPPING[char]
            room_name = f"{room_type.value}"
            room = Room(room_name, x, y, room_type)
            ship_map.add_room(room)

    # Connect adjacent rooms (up, down, left, right)
    for y in range(height):
        for x in range(width):
            room = ship_map.room_grid[y][x]
            if not room:
                continue
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= ny < height and 0 <= nx < width:
                    neighbor = ship_map.room_grid[ny][nx]
                    if neighbor:
                        room.connect(neighbor)

    return ship_map


def create_vents_from_list(smap: ShipMap, layout: List[tuple[tuple[int, int], tuple[int, int]]]) -> None:
    for room1_coords, room2_coords in layout:
        smap.connect_rooms_vents(room1_coords, room2_coords)
