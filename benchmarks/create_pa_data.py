#!/usr/bin/env python3

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from spinedb_api import DatabaseMapping

DB_URL = "sqlite:///../databases/BB_data.sqlite"

with DatabaseMapping(DB_URL) as db:
    item = db.get_parameter_value_item(id=256351)

parsed_dict = item["parsed_value"].to_dict()

data = {}

for index, name in enumerate(["f00", "avg", "scen", "median"]):
    data[name] = parsed_dict["data"][index][1]["data"]

my_type = pa.map_(pa.string(), pa.float64())

def create_map_scalar(data):
    key_array = pa.array([x[0] for x in data])
    value_array = pa.array([x[1] for x in data])
    return pa.scalar(list(zip(key_array, value_array)), type=my_type)

struct_scalar = pa.scalar({
    "f00": create_map_scalar(data["f00"]),
    "avg": create_map_scalar(data["avg"]),
    "scen": create_map_scalar(data["scen"]),
    "median": create_map_scalar(data["median"]),
    }, type=pa.struct([
        ("f00", my_type),
        ("avg", my_type),
        ("scen", my_type),
        ("median", my_type),
        ]))

table = pa.Table.from_arrays([pa.array([struct_scalar])], names=["data"])

pq.write_table(table, "../databases/data.parquet")
