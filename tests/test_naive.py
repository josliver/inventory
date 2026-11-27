from collections.abc import Iterator
from contextlib import closing
from pathlib import Path
from sqlite3 import Connection, connect

import pytest
from data_builder import a_movement

from inventory.movement import MovementType
from inventory.naive import create_schema, record_movement, save_stock, stock_of


class StoreSpy:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []

    def __call__(self, sku: str, stock: int) -> None:
        self.calls.append((sku, stock))


def ignore_store(sku: str, stock: int) -> None:
    pass


@pytest.fixture
def conn(tmp_path: Path) -> Iterator[Connection]:
    connection = connect(tmp_path / "inventory.db", autocommit=False)
    create_schema(connection)
    yield connection
    connection.close()


def test_entry_for_new_product_creates_stock(conn: Connection) -> None:
    movement = a_movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    record_movement(connection=conn, movement=movement, notify_store=ignore_store)

    assert stock_of(conn, "ABC-1") == 5


def test_exit_exceeding_stock_is_rejected_and_stock_unchanged(conn: Connection) -> None:
    save_stock(conn, "ABC-1", 2)
    movement = a_movement(sku="ABC-1", kind=MovementType.OUT, quantity=5)

    with pytest.raises(ValueError):
        record_movement(connection=conn, movement=movement, notify_store=ignore_store)

    assert stock_of(conn, "ABC-1") == 2


def test_store_is_notified_with_remaining_stock(conn: Connection) -> None:
    save_stock(conn, "ABC-1", 10)
    store = StoreSpy()

    record_movement(
        connection=conn,
        movement=a_movement(sku="ABC-1", kind=MovementType.OUT, quantity=3),
        notify_store=store,
    )
    record_movement(
        connection=conn,
        movement=a_movement(sku="NEW-1", kind=MovementType.IN, quantity=2),
        notify_store=store,
    )

    assert store.calls == [("ABC-1", 7), ("NEW-1", 2)]


def test_store_is_not_notified_when_movement_is_rejected(conn: Connection) -> None:
    # stock = {"ABC-1": 2}
    save_stock(conn, "ABC-1", 2)
    store = StoreSpy()

    with pytest.raises(ValueError):
        record_movement(
            connection=conn,
            movement=a_movement(sku="ABC-1", kind=MovementType.OUT, quantity=5),
            notify_store=store,
        )

    assert store.calls == []


def test_movements_accumulate_on_existing_product(conn: Connection) -> None:
    save_stock(conn, "ABC-1", 10)
    save_stock(conn, "XYZ-9", 4)
    movement = a_movement(sku="ABC-1", kind=MovementType.OUT, quantity=3)

    record_movement(conn, movement, notify_store=ignore_store)

    assert stock_of(conn, "ABC-1") == 7
    assert stock_of(conn, "XYZ-9") == 4


def test_stock_of_unknown_product_is_zero(conn: Connection) -> None:
    assert stock_of(conn, "NOPE-1") == 0


def test_saved_stock_can_be_read(conn: Connection) -> None:
    save_stock(conn, "ABC-1", 5)

    assert stock_of(conn, "ABC-1") == 5


def test_save_stock_overwrites_previous_value(conn: Connection) -> None:
    save_stock(conn, "ABC-1", 5)
    save_stock(conn, "ABC-1", 2)

    assert stock_of(conn, "ABC-1") == 2


def test_each_movement_is_committed(conn: Connection, tmp_path: Path) -> None:
    movement = a_movement(sku="ABC-1", kind=MovementType.IN, quantity=5)

    record_movement(conn, movement, notify_store=ignore_store)

    with closing(connect(tmp_path / "inventory.db")) as other:
        assert stock_of(other, "ABC-1") == 5
