import datetime
import math
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


def run_map_10_10_10_10(parameters):
    def to_db_map_10_10_10_10():
        return to_database(parameters["function"](parameters["dimensions"]))
    def from_db_map_10_10_10_10(db_value, value_type):
        _ = from_database(db_value, value_type)

    db_value, value_type = to_db_map_10_10_10_10()
    from_db_map_10_10_10_10(db_value, value_type)

def run_map_10_100_10(parameters):
    def to_db_map_10_100_10():
        return to_database(parameters["function"](parameters["dimensions"]))
    def from_db_map_10_100_10(db_value, value_type):
        _ = from_database(db_value, value_type)

    db_value, value_type = to_db_map_10_100_10()
    from_db_map_10_100_10(db_value, value_type)

def run_map_100_100(parameters):
    def to_db_map_100_100():
        return to_database(parameters["function"](parameters["dimensions"]))
    def from_db_map_100_100(db_value, value_type):
        _ = from_database(db_value, value_type)

    db_value, value_type = to_db_map_100_100()
    from_db_map_100_100(db_value, value_type)

def run_map_10000(parameters):
    def to_db_map_10000():
        return to_database(parameters["function"](parameters["dimensions"]))
    def from_db_map_10000(db_value, value_type):
        _ = from_database(db_value, value_type)

    db_value, value_type = to_db_map_10000()
    from_db_map_10000(db_value, value_type)

def run_time_series_variable(parameters):
    def to_db_time_series_variable():
        return to_database(parameters["function"](parameters["dimensions"]))
    def from_db_time_series_variable(db_value, value_type):
        _ = from_database(db_value, value_type)

    db_value, value_type = to_db_time_series_variable()
    from_db_time_series_variable(db_value, value_type)

def run_time_series_fixed(parameters):
    def to_db_time_series_fixed():
        return to_database(parameters["function"](parameters["dimensions"]))
    def from_db_time_series_fixed(db_value, value_type):
        _ = from_database(db_value, value_type)

    db_value, value_type = to_db_time_series_fixed()
    from_db_time_series_fixed(db_value, value_type)


if __name__ == "__main__":
    RUNS = {
        "from_database[Map(10, 10, 10, 10)]": {
            "function": build_even_map,
            "dimensions": (10, 10, 10, 10),
            },
        "from_database[Map(10, 100, 10)]": {
            "function": build_even_map,
            "dimensions": (10, 100, 10),
            },
        "from_database[Map(100, 100)]": {
            "function": build_even_map,
            "dimensions": (100, 100),
            },
        "from_database[Map(10000)]": {
            "function": build_even_map,
            "dimensions": (10000,),
            },
        "from_database[TimeSeriesVariableResolution(10000)]": {
            "function": build_time_series_variable,
            "dimensions": 10000,
            },
        "from_database[TimeSeriesFixedResolution(10000)]": {
            "function": build_time_series_fixed,
            "dimensions": 10000,
            },
    }

    run_map_10_10_10_10(parameters=RUNS["from_database[Map(10, 10, 10, 10)]"])
    run_map_10_100_10(parameters=RUNS["from_database[Map(10, 100, 10)]"])
    run_map_100_100(parameters=RUNS["from_database[Map(100, 100)]"])
    run_map_10000(parameters=RUNS["from_database[Map(10000)]"])
    run_time_series_variable(parameters=RUNS["from_database[TimeSeriesVariableResolution(10000)]"])
    run_time_series_fixed(parameters=RUNS["from_database[TimeSeriesFixedResolution(10000)]"])
