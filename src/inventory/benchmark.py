import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from inventory.movement import Movement, MovementType


@dataclass(frozen=True, slots=True, kw_only=True)
class Measurement:
    count: int
    seconds: float

    @property
    def rate(self) -> int:
        return int(self.count / self.seconds)


def measure(
    movements: Iterable[Movement],
    record: Callable[[Movement], None],
    *,
    clock: Callable[[], float] = time.perf_counter,
) -> Measurement:
    count = 0
    start = clock()
    for count, movement in enumerate(movements, start=1):
        record(movement)

    seconds = clock() - start
    return Measurement(count=count, seconds=seconds)


if __name__ == "__main__":
    movements = [Movement(sku="ABC-1", kind=MovementType.IN, quantity=1)] * 3
    print(measure(movements, record=lambda movement: None, clock=time.perf_counter))
