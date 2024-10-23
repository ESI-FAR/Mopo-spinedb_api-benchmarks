SETUP="
import adbc_driver_sqlite.dbapi
import json
import timeit
from spinedb_api import DatabaseMapping


def get_datapoint(DB_URL):
    with adbc_driver_sqlite.dbapi.connect('file:'+DB_URL) as connection:
        with connection.cursor() as cur:
            cur.execute('SELECT value from parameter_value WHERE id=256351')
            table = cur.fetch_arrow_table()

    return json.loads(table['value'][0].as_py())['data'][2][1]['data'][-1][-1]
"

echo
echo "=== Benchmarking ADBC by ID. ==="
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
