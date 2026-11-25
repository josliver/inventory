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

@pytest.mark.parametrize(
    "sku, kind, quantity, expected",
    [
        pytest.param("ABC-1", MovementType.IN, 0, "No valid quantity (Zero)", id="quantity-non-valid-zero"),
        pytest.param("ABC-1", MovementType.IN, -1, "No valid quantity (Negative IN)", id="quantity-non-valid-neg-in"),
        pytest.param("ABC-1",MovementType.OUT, -1, "No valid quantity (Negative OUT)", id="quantity-non-valid-neg-out"),
        pytest.param("",MovementType.IN, 5, "", id="sku-non-valid-empty"),
        pytest.param("     ", MovementType.OUT, 12, -12, id="sku-non-valid-spaces")
    ],
)
def test_movement_exceptions(sku: str, kind: MovementType, quantity: int, expected: str) -> None:
    with pytest.raises(ValueError, match=expected):
        Movement(sku=sku, kind=kind,quantity=quantity)