#!/usr/bin/env python3

from spinedb_api import DatabaseMapping

def bb_data():
    db = DatabaseMapping(f"sqlite:///databases/BB_data.sqlite")
    vals = list(db.get_items(item_type="parameter_value"))
    db.close()

def egypt():
    db = DatabaseMapping(f"sqlite:///databases/egypt-national.sqlite")
    vals = list(db.get_items(item_type="parameter_value"))
    print(vals)
    db.close()

#bb_data()
egypt()
