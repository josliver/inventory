from collections.abc import Callable

from inventory.movement import Movement
from inventory.stock import new_stock


def record_movement(
    stock: dict[str, int],
    movement: Movement,
    *,
    notify_store: Callable[[str, int], None],
) -> None:
    current = stock.get(movement.sku, 0)
    updated = new_stock(current=current, delta=movement.delta)

    stock[movement.sku] = updated

    notify_store(movement.sku, updated)


def create_schema():
    pass

def save_stock():
    pass

def stock_of():
    pass