import pytest

from inventory.movement import Movement, MovementType
from inventory.naive import record_movement


def test_entry_for_new_product_creates_stock() -> None:
    stock: dict[str, int] = {}
    movement = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    record_movement(stock, movement)

    assert stock == {"ABC-1": 5}


def test_movements_accumulate_on_existing_product() -> None:
    stock = {"ABC-1": 10, "XYZ-9": 4}
    movement = Movement(sku="ABC-1", kind=MovementType.OUT, quantity=3)

    record_movement(stock, movement)

    assert stock == {"ABC-1": 7, "XYZ-9": 4}


def test_exit_exceeding_stock_is_rejected_and_stock_unchanged() -> None:
    stock = {"ABC-1": 2}
    movement = Movement(sku="ABC-1", kind=MovementType.OUT, quantity=5)

    with pytest.raises(ValueError):
        record_movement(stock, movement)

    assert stock == {"ABC-1": 2}
