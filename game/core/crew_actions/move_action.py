from typing import Callable
from .base_action import BaseAction
from interfaces import ICrewMember, IRoom

class MoveAction(BaseAction):
    def __init__(self, plan_movement_callback: Callable):
        self.name = "Move"
        self.cost = 1
        self._callback = plan_movement_callback

    def perform(self, actor: ICrewMember, room: IRoom, **kwargs) -> None:
        get_input = kwargs.get("get_input")
        coords = get_input("Enter target coordinates (x y): ")
        try:
            x, y = map(int, coords.split())
            self._callback(actor, (x, y))
            print(f"{actor.name} plans to move to ({x}, {y}).")
        except Exception:
            print("Invalid coordinates.")