SETUP="
from spinedb_api import DatabaseMapping
import timeit

#DB_URL = 'sqlite:///../databases/BB_data.sqlite'
#DB_URL = 'sqlite:///../databases/BB_data_stripped.sqlite'
#DB_URL = 'sqlite:////tmp/ramdisk/BB_data.sqlite'
#DB_URL = 'sqlite:////tmp/ramdisk/BB_data_stripped.sqlite'

def get_datapoint(DB_URL):
    with DatabaseMapping(DB_URL) as db:
        item = db.get_parameter_value_item(id=256351)

    return item['parsed_value'].values[2].values[-1]
"

echo "Benchmarking SpineDB API by ID."
for db in \
  'sqlite:///../databases/BB_data.sqlite' \
  'sqlite:///../databases/BB_data_stripped.sqlite' \
  'sqlite:///../databases/ramdisk/BB_data.sqlite' \
  'sqlite:///../databases/ramdisk/BB_data_stripped.sqlite' \
  ; do
  echo
  echo "Using $db"
  python3 -m timeit -r 50 -s "$SETUP" "get_datapoint('$db')"
done
