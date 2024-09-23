#!/usr/bin/env python3

from spinedb_api import DatabaseMapping, from_database
from spinetoolbox.plotting import turn_node_to_xy_data

DB_URL = "sqlite:///databases/BB_data.sqlite"
#DB_URL = "sqlite:///databases/egypt-national.sqlite"

db = DatabaseMapping(f"sqlite:///databases/BB_data.sqlite")
vals = list(db.get_items(item_type="parameter_value"))
db.close()
