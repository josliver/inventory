from dataclasses import dataclass
from enum import StrEnum, auto
from typing import assert_never


class MovementType(StrEnum):
    IN = auto()
    OUT = auto()


@dataclass(frozen=True, slots=True, kw_only=True)
class Movement:
    sku: str
    warehouse: str
    kind: MovementType
    quantity: int

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("Invalid sku: must not be empty or blank")

        if not self.warehouse.strip():
            raise ValueError("warehouse")

        if self.quantity <= 0:
            raise ValueError(f"Invalid quantity: must be positive, got {self.quantity}")

    @property
    def delta(self) -> int:
        match self.kind:
            case MovementType.IN:
                return self.quantity
            case MovementType.OUT:
                return -self.quantity
            case _:
                assert_never(self.kind)
