import tempfile
from collections.abc import Callable
from contextlib import closing
from pathlib import Path
from sqlite3 import connect

from inventory.benchmark import Measurement, make_slow_store, measure
from inventory.movement import Movement, MovementType
from inventory.naive import create_schema, record_movement

TOP_MOVEMENTS: int = 300
DB_NAME: str = "data.db"


def run(store: Callable[[str, int], None]) -> Measurement:

    with (
        tempfile.TemporaryDirectory() as tmp,
        closing(connect(Path(tmp) / DB_NAME, autocommit=False)) as conn,
    ):
        create_schema(conn)
        movements: list[Movement] = [
            Movement(sku=f"SKU-{i % 10}", kind=MovementType.IN, quantity=3)
            for i in range(TOP_MOVEMENTS)
        ]

        record = lambda movement: record_movement(conn, movement, notify_store=store)

        return measure(movements=movements, record=record)


if __name__ == "__main__":
    print("---------- [START] ----------")
    first_run = run(make_slow_store(0.04))
    print(
        f"With slow store (40 ms) results: {first_run.count} movements and {first_run.seconds:.2f} sec and a rate of {first_run.rate:.1f} mov/s"
    )
    second_run = run(lambda x, y: None)
    print(
        f"Without store results: {second_run.count} movements and {second_run.seconds:.2f} sec and a rate of {second_run.rate:.1f} mov/s"
    )
    print("---------- [END] ----------")
