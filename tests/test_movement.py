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
        pytest.param(MovementType.OUT, 12, -12, id="exit-other-quantity"),
    ],
)
def test_calculate_delta(kind: MovementType, quantity: int, expected: int) -> None:
    movement = Movement(sku="ABC-1", kind=kind, quantity=quantity)

    assert movement.delta == expected


@pytest.mark.parametrize(
    "quantity, expected",
    [
        pytest.param(
            0,
            "Invalid quantity: must be positive, got 0",
            id="quantity-zero",
        ),
        pytest.param(
            -1,
            "Invalid quantity: must be positive, got -1",
            id="quantity-neg",
        ),
    ],
)
def test_non_positive_quantity_is_rejected(quantity: int, expected: str) -> None:
    with pytest.raises(ValueError, match=re.escape(expected)):
        Movement(sku="sku-01", kind=MovementType.IN, quantity=quantity)


@pytest.mark.parametrize(
    "sku",
    [
        pytest.param(
            "",
            id="sku-non-valid-empty",
        ),
        pytest.param(
            "     ",
            id="sku-non-valid-spaces",
        ),
    ],
)
def test_blank_sku_is_rejected(sku: str) -> None:
    with pytest.raises(ValueError, match="Invalid sku: must not be empty or blank"):
        Movement(sku=sku, kind=MovementType.IN, quantity=10)


def test_movements_with_same_values_are_equal() -> None:
    m1 = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)
    m2 = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    assert m1 == m2
