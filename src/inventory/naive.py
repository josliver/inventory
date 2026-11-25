from inventory.movement import Movement
from inventory.stock import new_stock


def record_movement(stock: dict[str, int], movement: Movement) -> None:
    current = stock.get(movement.sku, 0)

    stock[movement.sku] = new_stock(current=current, delta=movement.delta)
