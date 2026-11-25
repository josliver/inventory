from inventory.naive import record_movement

from inventory.movement import Movement, MovementType


def test_entry_for_new_product_creates_stock() -> None:
    stock: dict[str, int] = {}
    movement = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    record_movement(stock, movement)

    assert stock == {"ABC-1": 5}