SETUP="
import adbc_driver_sqlite.dbapi
import json
import timeit
from spinedb_api import DatabaseMapping


def get_datapoint(DB_URL):
    with adbc_driver_sqlite.dbapi.connect('file:'+DB_URL) as connection:
        with connection.cursor() as cur:
            cur.execute('SELECT json_extract(parameter_value.value, \'$.scen[#-1].v\') FROM parameter_value WHERE id=256351;')
            table = cur.fetch_arrow_table()

    return table[0][0].as_py()
"

echo
echo "=== Benchmarking ADBC with a queryable JSON structure. ==="
for db in \
  ../databases/BB_data.sqlite \
  ../databases/BB_data_stripped.sqlite \
  ../databases/BB_data_stripped_queryable.sqlite \
  ../databases/ramdisk/BB_data.sqlite \
  ../databases/ramdisk/BB_data_stripped.sqlite \
  ../databases/ramdisk/BB_data_stripped_queryable.sqlite \
  ; do
  echo
  echo "Using $db"
  python3 -m timeit -r 50 -s "$SETUP" "get_datapoint('$db')"
done
