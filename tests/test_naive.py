import pytest

from inventory.movement import Movement, MovementType
from inventory.naive import record_movement


class StoreSpy:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []

    def __call__(self, sku: str, stock: int) -> None:
        self.calls.append((sku, stock))


def ignore_store(sku: str, stock: int) -> None:
    pass


def test_entry_for_new_product_creates_stock() -> None:
    stock: dict[str, int] = {}
    movement = Movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    record_movement(stock=stock, movement=movement, notify_store=ignore_store)

    assert stock == {"ABC-1": 5}


def test_movements_accumulate_on_existing_product() -> None:
    stock = {"ABC-1": 10, "XYZ-9": 4}
    movement = Movement(sku="ABC-1", kind=MovementType.OUT, quantity=3)

    record_movement(stock=stock, movement=movement, notify_store=ignore_store)

    assert stock == {"ABC-1": 7, "XYZ-9": 4}


def test_exit_exceeding_stock_is_rejected_and_stock_unchanged() -> None:
    stock = {"ABC-1": 2}
    movement = Movement(sku="ABC-1", kind=MovementType.OUT, quantity=5)

    with pytest.raises(ValueError):
        record_movement(stock=stock, movement=movement, notify_store=ignore_store)

    assert stock == {"ABC-1": 2}


def test_store_is_notified_with_remaining_stock() -> None:
    stock = {"ABC-1": 10}
    store = StoreSpy()

    record_movement(
        stock=stock,
        movement=Movement(sku="ABC-1", kind=MovementType.OUT, quantity=3),
        notify_store=store,
    )
    record_movement(
        stock=stock,
        movement=Movement(sku="NEW-1", kind=MovementType.IN, quantity=2),
        notify_store=store,
    )

    assert store.calls == [("ABC-1", 7), ("NEW-1", 2)]


def test_store_is_not_notified_when_movement_is_rejected() -> None:
    stock = {"ABC-1": 2}
    store = StoreSpy()

    with pytest.raises(ValueError):
        record_movement(
            stock=stock,
            movement=Movement(sku="ABC-1", kind=MovementType.OUT, quantity=5),
            notify_store=store,
        )

    assert store.calls == []
