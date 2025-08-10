# actions/peek_action.py
from .base_action import BaseAction
import random

class PeekAction(BaseAction):
    def __init__(self):
        super().__init__("Peek", cost=1)

    def is_available(self, actor, room) -> bool:
        return bool(room.connections)  # Can only peek if there are adjacent rooms

    def perform(self, actor, room, **kwargs):
        print("\nChoose a room to peek into:")
        for idx, neighbor in enumerate(room.connections):
            print(f"{idx + 1}. {neighbor.name}")
        print("0. Cancel")

        choice = kwargs.get("get_input")("Your choice: ")
        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(room.connections):
                target_room = room.connections[idx]
                if getattr(target_room, "has_alien", False):
                    print(f"{actor.name} peeks into {target_room.name}... ALIEN SPOTTED!")
                else:
                    print(f"{actor.name} peeks into {target_room.name}... all clear.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
