import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from inventory.movement import Movement


@dataclass(frozen=True, slots=True, kw_only=True)
class Measurement:
    count: int
    seconds: float

    @property
    def rate(self) -> float:
        return self.count / self.seconds


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


def make_slow_store(
    delay: float,
    *,
    sleep: Callable[
        [
            float,
        ],
        None,
    ] = time.sleep,
) -> Callable[[str, int], None]:

    def slow_store(sku: str, stock: int) -> None:
        sleep(delay)

    return slow_store
