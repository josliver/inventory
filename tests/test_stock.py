import pytest

from inventory.stock import new_stock


@pytest.mark.parametrize("current, delta, expected", 
                         [pytest.param(10,5,15, id="Increase Stock"),
                          pytest.param(10,-3,7, id="Decrease Stock"),
                          pytest.param(10,0,10, id="Nothing Added in Stock"),
                          pytest.param(10,-10,0, id="Break in Stock")
                          ])

def test_new_stock(current:int, delta:int, expected:int) -> None:
    assert new_stock(current=current, delta=delta) == expected

def test_negative_stock() -> None:
    with pytest.raises(ValueError, match="Negative Inventory"):
        new_stock(current=2, delta=-5)
