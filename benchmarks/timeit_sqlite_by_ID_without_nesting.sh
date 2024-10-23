SETUP="
import json
import sqlite3
import timeit

def get_datapoint(DB_URL):
    with sqlite3.connect(DB_URL) as con:
        cur = con.cursor()
        item = cur.execute('SELECT value from parameter_value WHERE id=256351')
        table = cur.fetchall()

    return json.loads(table[0][0])['scen'][-1][-1]
"

echo "Benchmarking SQlite by ID without nesting."
for db in \
  ../databases/BB_data_stripped_flat.sqlite \
  ../databases/ramdisk/BB_data_stripped_flat.sqlite \
  ; do
  echo
  echo "Using $db"
  python3 -m timeit -r 50 -s "$SETUP" "get_datapoint('$db')"
done
