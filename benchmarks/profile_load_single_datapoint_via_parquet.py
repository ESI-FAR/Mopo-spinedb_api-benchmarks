#!/usr/bin/env python3

import pyarrow.parquet as pq

DB_URL = "../databases/data.parquet"

def get_item(DB_URL):
    return pq.read_table(DB_URL)

def get_value(table):
    return table["data"][0]["scen"][-1][1]

table = get_item(DB_URL)
data_point = get_value(table)
