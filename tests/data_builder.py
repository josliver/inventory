from inventory.movement import Movement, MovementType


def a_movement(
    *, sku="ABC-1", warehouse="MAIN", kind=MovementType.IN, quantity=5
) -> Movement:
    """
    Patrón Test Data Builder
    """
    return Movement(sku=sku, warehouse=warehouse, kind=kind, quantity=quantity)
