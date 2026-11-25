import dataclasses
import re

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

@pytest.mark.parametrize(
    "sku, kind, quantity, expected",
    [
        pytest.param("ABC-1", MovementType.IN, 0, "Invalid quantity (Zero)", id="quantity-non-valid-zero-in"),
        pytest.param("ABC-1", MovementType.OUT, 0, "Invalid quantity (Zero)", id="quantity-non-valid-zero-out"),
        pytest.param("ABC-1", MovementType.IN, -1, "Invalid quantity (Negative)", id="quantity-non-valid-neg-in"),
        pytest.param("ABC-1",MovementType.OUT, -1, "Invalid quantity (Negative)", id="quantity-non-valid-neg-out"),
        pytest.param("",MovementType.IN, 5, "Invalid sku: must not be empty or blank", id="sku-non-valid-empty"),
        pytest.param("     ", MovementType.OUT, 12, "Invalid sku: must not be empty or blank", id="sku-non-valid-spaces")
    ],
)
def test_movement_exceptions(sku: str, kind: MovementType, quantity: int, expected: str) -> None:
    with pytest.raises(ValueError, match=re.escape(expected)):
        Movement(sku=sku, kind=kind,quantity=quantity)

def test_movements_compare() -> None:
    m1 = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)
    m2 = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    assert m1 == m2