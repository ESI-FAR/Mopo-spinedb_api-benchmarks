#!/usr/bin/env python3

from spinedb_api import DatabaseMapping

DB_URL = "sqlite:///../databases/BB_data.sqlite"

def get_item(DB_URL):
    with DatabaseMapping(DB_URL) as db:
        item = db.get_parameter_value_item(id=256351)
    return item

def parse_values(item):
    return item["parsed_value"]

def get_value(parsed_value):
    return parsed_value.values[2].values[-1]

item = get_item(DB_URL)
parsed_value = parse_values(item)
data_point = get_value(parsed_value)
