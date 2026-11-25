import dataclasses

import pytest

from inventory.movement import Movement, MovementType


def test_movement_is_immutable() -> None:
    movement = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    with pytest.raises(dataclasses.FrozenInstanceError):
        movement.quantity = 10  # type: ignore[misc]
