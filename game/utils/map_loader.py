from typing import List, Dict
from ..core.ship_map import ShipMap
from ..core.room import Room
from ..enums.room_type import RoomType


ROOM_TYPE_MAPPING: Dict[str, RoomType] = {
    "1": RoomType.BRIDGE,
    "2": RoomType.LIVING_QUARTERS,
    "3": RoomType.GREENHOUSE,
    "4": RoomType.MEDBAY,
    "5": RoomType.POWER_GENERATOR,
    "6": RoomType.OXYGEN_GENERATOR,
    "7": RoomType.GENERIC
}


def create_map_from_text(layout: List[str]) -> ShipMap:
    height = len(layout)
    width = max(len(row) for row in layout)
    ship_map = ShipMap(width, height)

    room_grid: List[List[Room | None]] = [[None for _ in range(width)] for _ in range(height)]

    # Create room instances
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if char == "0":
                continue
            if char not in ROOM_TYPE_MAPPING:
                raise ValueError(f"Invalid room type symbol: '{char}' at ({x}, {y})")
            room_type = ROOM_TYPE_MAPPING[char]
            room_name = f"{room_type.value} ({x},{y})"
            room = Room(room_name, x, y, room_type)
            ship_map.add_room(room)
            room_grid[y][x] = room

    # Connect adjacent rooms (up, down, left, right)
    for y in range(height):
        for x in range(width):
            room = room_grid[y][x]
            if not room:
                continue
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= ny < height and 0 <= nx < width:
                    neighbor = room_grid[ny][nx]
                    if neighbor:
                        room.connect(neighbor)

    return ship_map
