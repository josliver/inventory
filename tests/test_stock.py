from inventory.stock import new_stock


def test_entry_increase_stock() -> None:
    assert new_stock(current=10, delta=5) == 15