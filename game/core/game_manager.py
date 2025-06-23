from typing import List
from .ship_map import ShipMap
from .room import Room
from ..enums import RoomType
from .crew_member import CrewMember
from .alien import Alien
from ..graphics import render_map
from ..config import MAP_WIDTH, MAP_HEIGHT
from ..interfaces import ICrewMember, IAlien


class GameManager:
    def __init__(self):
        self.map: ShipMap = self._create_map()
        self.crew: List[ICrewMember] = [
            CrewMember("Alice", self.map.get_room(0, 0)),
            CrewMember("Bob", self.map.get_room(1, 0)),
            CrewMember("Charlie", self.map.get_room(0, 1)),
        ]
        self.alien: IAlien = Alien(self.map.get_room(2, 2))

    def _create_map(self) -> ShipMap:
        smap = ShipMap(MAP_WIDTH, MAP_HEIGHT)

        bridge = Room("Bridge", 0, 0, RoomType.BRIDGE)
        medbay = Room("Medbay", 0, 2, RoomType.MEDBAY)
        greenhouse = Room("Greenhouse", 0, 4, RoomType.GREENHOUSE)
        power_generator = Room("Power Generator", 2, 0, RoomType.POWER_GENERATOR)
        oxygen_generator = Room("Oxygen Generator", 2, 4, RoomType.OXYGEN_GENERATOR)
        generic_room_1 = Room("Generic Room 1", 4, 0, RoomType.GENERIC)
        living_quarters_1 = Room("Living Quarters 1", 4, 2, RoomType.LIVING_QUARTERS)
        living_quarters_2 = Room("Living Quarters 2", 4, 4, RoomType.LIVING_QUARTERS)


        for room in [bridge, 
                     medbay, 
                     greenhouse, 
                     power_generator, 
                     oxygen_generator, 
                     generic_room_1, 
                     living_quarters_1, 
                     living_quarters_2]:
            smap.add_room(room)

        bridge.connect(medbay)
        bridge.connect(power_generator)
        power_generator.connect(generic_room_1)
        medbay.connect(greenhouse)
        greenhouse.connect(oxygen_generator)
        oxygen_generator.connect(living_quarters_2)
        living_quarters_2.connect(living_quarters_1)
        living_quarters_1.connect(generic_room_1)

        medbay.connect_vent(oxygen_generator)
        oxygen_generator.connect_vent(living_quarters_1)
        living_quarters_1.connect_vent(generic_room_1)
        generic_room_1.connect_vent(medbay)

        # Optional: manually add vent connections here later

        return smap

    def run(self) -> None:
        while True:
            render_map(self.map, self.crew, self.alien)
            input("\n[Press Enter to continue]")
