def new_stock(*,current: int, delta: int) -> int:
    stock: int = current + delta
    if stock< 0:
        raise ValueError(f"Negative Inventory, current: {current} - delta: {delta}")
        
    return stock
