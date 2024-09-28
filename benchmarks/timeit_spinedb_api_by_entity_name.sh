SETUP="
from spinedb_api import DatabaseMapping
import timeit

DB_URL = 'sqlite:////tmp/ramdisk/BB_data.sqlite'

def get_datapoint(DB_URL):
    with DatabaseMapping(DB_URL) as db:
        item = db.get_items('parameter_value', entity_name='flow__node_wind__80NO')[0]

    return item['parsed_value'].values[2].values[-1]
"

python3 -m timeit -r 50 -s "$SETUP" "get_datapoint(DB_URL)"
