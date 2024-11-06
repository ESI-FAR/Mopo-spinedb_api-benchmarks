SETUP="
import adbc_driver_sqlite.dbapi
import json
import timeit
from spinedb_api import DatabaseMapping


def get_datapoint(DB_URL):
    with adbc_driver_sqlite.dbapi.connect('file:'+DB_URL) as connection:
        with connection.cursor() as cur:
            cur.execute('SELECT json_extract(parameter_value.value, \'$.scen[#-1][#-1]\') FROM parameter_value WHERE id=256351;')
            table = cur.fetch_arrow_table()

    #print(table[0][0].as_py())
    return table[0][0].as_py()
"

echo
echo "=== Benchmarking ADBC by ID, querying JSON list. ==="
for db in \
  ../databases/BB_data_stripped_flat_list.sqlite \
  ../databases/ramdisk/BB_data_stripped_flat_list.sqlite \
  ; do
  echo
  echo "Using $db"
  python3 -m timeit -r 50 -s "$SETUP" "get_datapoint('$db')"
done
