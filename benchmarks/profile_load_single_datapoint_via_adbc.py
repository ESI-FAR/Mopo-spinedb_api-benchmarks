#!/usr/bin/env python3

import adbc_driver_manager.dbapi
import adbc_driver_sqlite.dbapi
import pyarrow as pa
import json

from spinedb_api import DatabaseMapping

DB_URL = "sqlite:///../databases/BB_data.sqlite"

def get_item(DB_URL):
    with adbc_driver_sqlite.dbapi.connect("file:"+"../databases/BB_data.sqlite") as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT value from parameter_value WHERE id=256351")
            table = cur.fetch_arrow_table()
    return table

def parse_values(item):
    return json.loads(item["value"][0].as_py())

def get_value(parsed_value):
    return parsed_value["data"][2][1]["data"][-1][-1]

item = get_item(DB_URL)
parsed_value = parse_values(item)
data_point = get_value(parsed_value)
