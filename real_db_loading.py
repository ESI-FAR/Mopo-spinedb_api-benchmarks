#!/usr/bin/env python3

from spinedb_api import DatabaseMapping, from_database
from spinetoolbox.plotting import turn_node_to_xy_data

DB_URL = "sqlite:///databases/BB_data.sqlite"
#DB_URL = "sqlite:///databases/egypt-national.sqlite"

#db = DatabaseMapping(DB_URL)
#value = db.get_parameter_value_item(id=256351)
#db.close()

#print(type(value))

#data = ast.literal_eval(value.__dict__["_mapped_item"]["value"].decode())

#data_0 = data["data"][0][1][1]["data"]  # f00
#data_1 = data["data"][1][1][1]["data"]  # avg
#data_2 = data["data"][2][1][1]["data"]  # scen
#data_3 = data["data"][3][1][1]["data"]  # median

#print(data_2[1]["data"][0])

#print(value["parsed_value"].values[2].values[-1])

def get_datapoint(DB_URL):
    with DatabaseMapping(DB_URL) as db:
        value = db.get_parameter_value_item(id=256351)

    print(value["parsed_value"].values[2].values[-1])

get_datapoint("sqlite:///databases/BB_data.sqlite")
