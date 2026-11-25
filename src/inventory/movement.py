import re
from dataclasses import dataclass
from enum import auto
from typing import assert_never

from strenum import StrEnum


class MovementType(StrEnum):
    IN = auto()
    OUT = auto()


@dataclass(frozen=True, slots=True, kw_only=True)
class Movement:
    sku: str
    kind: MovementType
    quantity: int

    def __post_init__(self):
        print ("ejecutado")
        if re.match(r"^\s*$", self.sku):
            raise ValueError("Invalid sku: must not be empty or blank")
        elif self.quantity == 0:
            raise ValueError("Invalid quantity (Zero)")
        elif self.quantity < 0:
            raise ValueError("Invalid quantity (Negative)")
        

    @property
    def delta(self) -> int:
        match self.kind:
            case MovementType.IN:
                return self.quantity
            case MovementType.OUT:
                return self.quantity * -1
            case _:
                assert_never(self.kind)
