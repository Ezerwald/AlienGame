from typing import Dict
from ..enums import RoomType

ROOM_TYPE_MAPPING: Dict[str, RoomType] = {
    "1": RoomType.BRIDGE,
    "2": RoomType.LIVING_QUARTERS,
    "3": RoomType.GREENHOUSE,
    "4": RoomType.MEDBAY,
    "5": RoomType.POWER_GENERATOR,
    "6": RoomType.OXYGEN_GENERATOR, 
    "7": RoomType.GENERIC
}