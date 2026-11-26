from inventory.benchmark import measure
from inventory.movement import Movement, MovementType


def test_measure_uses_clock_to_compute_elapsed_seconds() -> None:
    movements = [Movement(sku="ABC-1", kind=MovementType.IN, quantity=1)] * 3
    fake_clock = iter([10.0, 12.5]).__next__

    result = measure(movements, record=lambda movement: None, clock=fake_clock)

    assert result.count == 3
    assert result.seconds == 2.5