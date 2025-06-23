from abc import ABC, abstractmethod
from .i_actor import IActor

class IAlien(IActor, ABC):
    @abstractmethod
    def use_biomass(self, amount: int) -> None:
        ...

    @abstractmethod
    def add_biomass(self, amount: int) -> None:
        ...

    @property
    @abstractmethod
    def biomass(self) -> int:
        ...

    @abstractmethod
    def attack(self, target: IActor) -> None:
        ...
