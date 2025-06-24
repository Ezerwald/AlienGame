from typing import List, Tuple
from ..interfaces import ICrewMember
from ..utils import get_user_input


class PlanningUIManager:
    def __init__(self, crew_group: List[ICrewMember]):
        self.crew_group = crew_group
        self.assigned_count: dict[str, int] = {m.name: 0 for m in crew_group}
        self.assigned_actions: dict[str, List[str]] = {m.name: [] for m in crew_group}

    def run(self, plan_movement_callback) -> None:
        while True:
            print("\nCrew Members (Initiative Group):")
            for idx, member in enumerate(self.crew_group):
                print(f"{idx + 1}. {member.name} ({self.assigned_count[member.name]}/2 actions)")

            print("0. Continue to next initiative group")
            choice = get_user_input("Select crew member by number: ")

            if choice == "0":
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.crew_group):
                    member = self.crew_group[idx]
                    self._crew_member_menu(member, plan_movement_callback)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Enter a valid number.")

    def _crew_member_menu(self, member: ICrewMember, plan_movement_callback):
        while self.assigned_count[member.name] < 2:
            print(f"\nActions for {member.name} ({self.assigned_count[member.name]}/2):")

            # Show previously planned actions
            if self.assigned_actions[member.name]:
                print("Already chosen actions:")
                for i, act in enumerate(self.assigned_actions[member.name], 1):
                    print(f"  {i}. {act}")
            else:
                print("No actions chosen yet.")

            print("\nAvailable options:")
            print("1. Move (x y)")
            print("2. Wait")
            print("0. Back to crew list")

            choice = get_user_input("Choose action: ")

            if choice == "0":
                break

            elif choice == "1":
                coords = get_user_input("Enter target coordinates (x y): ")
                try:
                    x, y = map(int, coords.split())
                    plan_movement_callback(member, (x, y))
                    self.assigned_count[member.name] += 1
                    self.assigned_actions[member.name].append(f"Move to ({x}, {y}) (action planned)")
                except Exception:
                    print("Invalid coordinates.")

            elif choice == "2":
                print(f"{member.name} waits.")
                self.assigned_count[member.name] += 1
                self.assigned_actions[member.name].append("Wait (action finished)")

            else:
                print("Unknown action.")
