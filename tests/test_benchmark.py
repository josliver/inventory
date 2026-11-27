from inventory.benchmark import Measurement, make_slow_store, measure
from inventory.movement import Movement, MovementType


def test_measure_uses_clock_to_compute_elapsed_seconds() -> None:
    movements = [Movement(sku="ABC-1", kind=MovementType.IN, quantity=1)] * 3
    fake_clock = iter([10.0, 12.5]).__next__

    result = measure(movements, record=lambda movement: None, clock=fake_clock)

    assert result.count == 3
    assert result.seconds == 2.5


def test_measure_records_each_movement_in_order() -> None:
    movements = [
        Movement(sku="ABC-1", kind=MovementType.IN, quantity=1),
        Movement(sku="XYZ-9", kind=MovementType.OUT, quantity=2),
        Movement(sku="ABC-1", kind=MovementType.IN, quantity=3),
    ]
    recorded: list[Movement] = []

    measure(movements, record=recorded.append, clock=iter([0.0, 1.0]).__next__)

    assert recorded == movements


def test_rate_is_movements_per_second() -> None:
    result = Measurement(count=300, seconds=12.5)

    assert result.rate == 24.0


def test_slow_store_waits_the_given_delay_on_each_call() -> None:
    sleeps: list[float] = []
    store = make_slow_store(0.04, sleep=sleeps.append)

    store("ABC-1", 5)
    store("XYZ-9", 0)

    assert sleeps == [0.04, 0.04]
