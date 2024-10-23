SETUP="
from spinedb_api import DatabaseMapping
import timeit

def get_datapoint(DB_URL):
    with DatabaseMapping('sqlite:///'+DB_URL) as db:
        item = db.get_items('parameter_value', entity_name='flow__node_wind__80NO')[0]

    return item['parsed_value'].values[2].values[-1]
"

echo
echo "=== Benchmarking SpineDB API by entity name. ==="
for db in \
  ../databases/BB_data.sqlite \
  ../databases/BB_data_stripped.sqlite \
  ../databases/ramdisk/BB_data.sqlite \
  ../databases/ramdisk/BB_data_stripped.sqlite \
  ; do
  echo
  echo "Using $db"
  python3 -m timeit -r 50 -s "$SETUP" "get_datapoint('$db')"
done
