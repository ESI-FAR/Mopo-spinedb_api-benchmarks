#!/usr/bin/env python3

from spinedb_api import DatabaseMapping

DB_URL = "sqlite:///../databases/BB_data.sqlite"

def get_item(DB_URL):
    with DatabaseMapping(DB_URL) as db:
        item = db.get_items("parameter_value", entity_name="flow__node_wind__80NO")[0]
    return item

def parse_values(item):
    return item["parsed_value"]

def get_value(parsed_value):
    return parsed_value.values[2].values[-1]

item = get_item(DB_URL)
parsed_value = parse_values(item)
data_point = get_value(parsed_value)
