import dataclasses

import pytest

from inventory.movement import Movement, MovementType


def test_movement_is_immutable() -> None:
    movement = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    with pytest.raises(dataclasses.FrozenInstanceError):
        movement.quantity = 10  # type: ignore[misc]

@pytest.mark.parametrize(
    "kind, quantity, expected",
    [
        pytest.param(MovementType.IN, 5, 5, id="entry-adds"),
        pytest.param(MovementType.OUT, 5, -5, id="exit-subtracts"),
        pytest.param(MovementType.OUT, 12, -12, id="exit-other-quantity")
    ],
)

def test_calculate_delta(kind: MovementType, quantity: int, expected: int) -> None:
    movement = Movement(sku="ABC-1", kind=kind, quantity=quantity)
    assert movement.delta == expected
