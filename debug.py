
from enum import Enum


class Unit(Enum):
    """
    Enum representing different storage units.
    """
    Go = "Go"
    Mo = "Mo"
    Ko = "Ko"

    @property
    def factor(self) -> int:
        """
        Returns the corresponding factor for unit conversion.
        """
        return {"Go": 1024 ** 3, "Mo": 1024 ** 2, "Ko": 1024}.get(self.value, 1024 ** 3)

    @classmethod
    def from_string(cls, unit_str: str) -> "Unit":
        """
        Converts a string representation to a Unit enum value.
        Defaults to 'Go' if an unsupported unit is provided.
        """
        try:
            return cls(unit_str)
        except ValueError:
            print(f"Unit '{unit_str}' not supported. Defaulting to 'Go'.")
            return cls.Go

x = Unit.from_string("Go")

