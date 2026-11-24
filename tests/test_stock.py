import pytest

from inventory.stock import new_stock


def test_entry_increase_stock() -> None:
    assert new_stock(current=10, delta=5) == 15

def test_decrease_stock() -> None:
    assert new_stock(current=10, delta=-3) == 3

def test_negative_stock() -> None:
    with pytest.raises(ValueError, match="Negative Inventory"):
        assert new_stock(current=2, delta=-5)