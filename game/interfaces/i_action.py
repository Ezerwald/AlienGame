# actions/base_action.py
from abc import ABC, abstractmethod

class IAction(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def cost(self) -> int:
        return 1

    @abstractmethod
    def is_available(self, actor, room) -> bool:
        pass

    @abstractmethod
    def perform(self, actor, room, **kwargs) -> None:
        pass
