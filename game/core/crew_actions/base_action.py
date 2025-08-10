from ...interfaces import IAction

class BaseAction(IAction):
    def __init__(self, name: str, cost: int = 1):
        self._name = name
        self._cost = cost

    @property
    def name(self) -> str:
        return self._name

    @property
    def cost(self) -> int:
        return self._cost

    def is_available(self, actor, room) -> bool:
        return True  # Default implementation — override in subclasses
