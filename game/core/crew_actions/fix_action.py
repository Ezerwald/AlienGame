
from .base_action import BaseAction

class FixAction(BaseAction):
    def __init__(self):
        super().__init__("Fix", cost=1)

    def is_available(self, actor, room) -> bool:
        return getattr(room, "damaged", False) and getattr(room, "repair_required", 0) > 0

    def perform(self, actor, room, **kwargs):
        if not self.is_available(actor, room):
            print(f"{actor.name} cannot fix this room right now.")
            return

        room.repair_required -= 1
        print(f"{actor.name} works on repairs in {room.name}. {room.repair_required} actions left.")

        if room.repair_required <= 0:
            room.damaged = False
            print(f"{room.name} has been fully repaired!")
