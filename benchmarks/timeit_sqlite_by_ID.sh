SETUP="
import json
import sqlite3
import timeit


def get_datapoint(DB_URL):
    with sqlite3.connect(DB_URL) as con:
        cur = con.cursor()
        item = cur.execute('SELECT value from parameter_value WHERE id=256351')
        table = cur.fetchall()

    return json.loads(table[0][0])['data'][2][1]['data'][-1][-1]
"

echo "Benchmarking SQlite by ID."
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
