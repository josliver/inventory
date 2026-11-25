from dataclasses import dataclass
from enum import auto

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
        pass

