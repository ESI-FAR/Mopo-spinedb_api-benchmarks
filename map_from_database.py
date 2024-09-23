"""
This benchmark tests the performance of reading a Map type value from database.
"""

import time
import json
from benchmarks.utils import build_even_map
from spinedb_api import from_database, to_database
from rich import print as pprint


#def value_from_database(loops, db_value, value_type):
#    duration = 0.0
#    for _ in range(loops):
#        start = time.perf_counter()
#        from_database(db_value, value_type)
#        duration += time.perf_counter() - start
#    return duration
#

def run_benchmark(file_name):
    runs = {
        "value_from_database[Map(10, 10, 100)]": {"dimensions": (2, 3, 4)},
        "value_from_database[Map(1000)]": {"dimensions": (10000,)},
    }
    for i, (name, parameters) in enumerate(runs.items()):
        db_value, value_type = to_database(build_even_map(parameters["dimensions"]))
        if i == 0:
            pprint(json.loads(db_value.decode()))
        from_database(db_value, value_type)

if __name__ == "__main__":
    run_benchmark("")
