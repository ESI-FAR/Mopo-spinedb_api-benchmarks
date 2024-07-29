#!/usr/bin/env python3

from spinedb_api import DatabaseMapping

db = DatabaseMapping(f"sqlite:///databases/BB_data.sqlite")
db.close()
