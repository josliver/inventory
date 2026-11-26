import sqlite3
from collections.abc import Callable

from inventory.movement import Movement
from inventory.stock import new_stock


def record_movement(
    conn: sqlite3.Connection,
    movement: Movement,
    *,
    notify_store: Callable[[str, int], None],
) -> None:
    # current = stock.get(movement.sku, 0)
    current = stock_of(conn, movement.sku)
    updated = new_stock(current=current, delta=movement.delta)

    # stock[movement.sku] = updated
    save_stock(conn, movement.sku, updated)

    notify_store(movement.sku, updated)


def create_schema(connection: sqlite3.Connection) -> None:

    create_table_script = """CREATE TABLE IF NOT EXISTS stock (
                             sku      TEXT PRIMARY KEY,
                             quantity INTEGER NOT NULL);
                          """
    # cursor = connection.cursor()

    connection.execute(create_table_script)
    connection.commit()


def save_stock(connection: sqlite3.Connection, sku: str, quantity: int) -> None:
    query = """INSERT INTO stock(sku, quantity) VALUES (?, ?)
               ON CONFLICT(sku) DO UPDATE SET quantity = excluded.quantity"""
    connection.execute(query, (sku, quantity))


def stock_of(connection: sqlite3.Connection, sku: str) -> int:
    cursor = connection.cursor()
    cursor.execute("SELECT quantity FROM stock WHERE sku = ?", (sku,))
    row = cursor.fetchone()

    return row[0] if row else 0
