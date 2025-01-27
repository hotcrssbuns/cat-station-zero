class Station:
    def __init__(self):
        self._oxygen = 100
        self._power = 100
        self._hull_integrity = 100
        self._crew_morale = 100

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
