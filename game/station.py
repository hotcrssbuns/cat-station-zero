from game.tasks import TaskManager


class Station:
    def __init__(self):
        self._oxygen = 100
        self._power = 100
        self._hull_integrity = 100
        self._crew_morale = 100
        self._spare_parts = 5
        self._power_cells = 5
        self._medical_supplies = 5
        self._crew_members = 3
        self.task_manager = TaskManager()
        self.turns_until_resources = 5

    @property
    def oxygen(self):
        return self._oxygen

    @property
    def power(self):
        return self._power

    @property
    def hull_integrity(self):
        return self._hull_integrity

    @property
    def crew_morale(self):
        return self._crew_morale

    @property
    def spare_parts(self):
        return self._spare_parts

    @property
    def power_cells(self):
        return self._power_cells

    @property
    def medical_supplies(self):
        return self._medical_supplies

    @property
    def crew_members(self):
        return self._crew_members

    def is_game_over(self) -> bool:
        return (
            self._oxygen <= 0
            or self._power <= 0
            or self._hull_integrity <= 0
            or self._crew_morale <= 0
        )

    def update_system(self, system_name: str, amount: float) -> None:
        if hasattr(self, f"_{system_name}"):
            current_value = getattr(self, f"_{system_name}")
            new_value = max(0, min(100, current_value + amount))
            setattr(self, f"_{system_name}", new_value)

    def get_status(self) -> dict:
        return {
            "oxygen": self.oxygen,
            "power": self.power,
            "hull integrity": self.hull_integrity,
            "crew morale": self.crew_morale,
        }

    def get_resources(self) -> dict:
        return {
            "spare parts": self.spare_parts,
            "power cells": self.power_cells,
            "medical supplies": self.medical_supplies,
            "crew members": self.crew_members,
        }

    def get_tasks(self):
        return self.task_manager.get_active_tasks()

    def add_random_task(self):
        self.task_manager.create_task()
