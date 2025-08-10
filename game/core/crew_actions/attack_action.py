from .base_action import BaseAction
import random

class AttackAction(BaseAction):
    def __init__(self):
        super().__init__("Attack", cost=1)

    def is_available(self, actor, room) -> bool:
        return getattr(room, "has_alien", False)  # Attack only if alien is present

    def perform(self, actor, room, **kwargs):
        hit_chance = 0.6  # Base chance to hit (can be modified later)
        if random.random() <= hit_chance:
            print(f"{actor.name} attacks the alien and hits!")
            room.alien_health -= 1
            if room.alien_health <= 0:
                room.has_alien = False
                print("Alien defeated!")
        else:
            print(f"{actor.name} attacks but misses.")
