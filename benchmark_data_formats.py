import datetime
import math
import pyperf
import time
from benchmarks.utils import build_even_map
from spinedb_api import DateTime, Map, TimeSeriesVariableResolution, TimeSeriesFixedResolution, from_database, to_database
from typing import Sequence


def build_time_series_fixed(size: int) -> TimeSeriesFixedResolution:
    start = datetime.datetime(year=2024, month=1, day=1)
    ys = []
    for i in range(size):
        x = i / size
        ys.append(math.sin(x * math.pi / 2.0) + x)
    resolution = "1D"
    return TimeSeriesFixedResolution(start=start, resolution=resolution, values=ys, ignore_year=False, repeat=False)


def build_time_series_variable(size: int) -> TimeSeriesVariableResolution:
    start = datetime.datetime(year=2024, month=1, day=1)
    xs = []
    ys = []
    for i in range(size):
        xs.append(DateTime(start + datetime.timedelta(hours=i)))
        x = i / size
        ys.append(math.sin(x * math.pi / 2.0) + x)
    return TimeSeriesVariableResolution(indexes=xs, values=ys, ignore_year=False, repeat=False)


def build_map(size: int) -> Map:
    start = datetime.datetime(year=2024, month=1, day=1)
    xs = []
    ys = []
    for i in range(size):
        xs.append(DateTime(start + datetime.timedelta(hours=i)))
        x = i / size
        ys.append(math.sin(x * math.pi / 2.0) + x)
    return Map(xs, ys)


def build_even_map(shape: Sequence[int] = (10, 10, 10)) -> Map:
    if not shape:
        return Map([], [], index_type=DateTime)
    if len(shape) == 1:
        return build_map(shape[0])
    xs = []
    ys = []
    for i in range(shape[0]):
        start = datetime.datetime(year=2024, month=1, day=1)
        xs.append(DateTime(start + datetime.timedelta(hours=i)))
        ys.append(build_even_map(shape[1:]))
    return Map(xs, ys)


def value_from_database(loops, db_value, value_type):
    duration = 0.0
    for _ in range(loops):
        start = time.perf_counter()
        from_database(db_value, value_type)
        duration += time.perf_counter() - start
    return duration


def run_benchmark(file_name):
    runner = pyperf.Runner(loops=3)
    runs = {
        "value_from_database[Map(10, 10, 10, 10)]": {
            "function": build_even_map,
            "dimensions": (10, 10, 10, 10),
            },
        "value_from_database[Map(10, 100, 10)]": {
            "function": build_even_map,
            "dimensions": (10, 100, 10),
            },
        "value_from_database[Map(100, 100)]": {
            "function": build_even_map,
            "dimensions": (100, 100),
            },
        "value_from_database[Map(10000)]": {
            "function": build_even_map,
            "dimensions": (10000,),
            },
        "value_from_database[TimeSeriesVariableResolution(10000)]": {
            "function": build_time_series_variable,
            "dimensions": 10000,
            },
        "value_from_database[TimeSeriesFixedResolution(10000)]": {
            "function": build_time_series_fixed,
            "dimensions": 10000,
            },
    }
    for name, parameters in runs.items():
        db_value, value_type = to_database(parameters["function"](parameters["dimensions"]))
        benchmark = runner.bench_time_func(
            name,
            value_from_database,
            db_value,
            value_type,
        )
        if file_name and benchmark is not None:
            pyperf.add_runs(file_name, benchmark)


if __name__ == "__main__":
    run_benchmark("")
