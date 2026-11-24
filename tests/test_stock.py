import pytest

from inventory.stock import new_stock

#uv run pytest -k stockout

@pytest.mark.parametrize("current, delta, expected", 
                         [pytest.param(10,5,15, id="entry-increases"),
                          pytest.param(10,-3,7, id="exit-decreases"),
                          pytest.param(10,0,10, id="zero-delta"),
                          pytest.param(10,-10,0, id="stockout")
                          ])

def test_new_stock(current:int, delta:int, expected:int) -> None:
    assert new_stock(current=current, delta=delta) == expected

def test_negative_stock() -> None:
    pattern = r"^Negative Inventory, current: \d - delta: -?\d$"
    with pytest.raises(ValueError, match=pattern):
        new_stock(current=2, delta=-5)
