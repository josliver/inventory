def new_stock(current: int, delta: int) -> int:
    stock: int = current + delta
    if stock >= 0:
        return stock
    else:
        raise ValueError("Negative Inventory")