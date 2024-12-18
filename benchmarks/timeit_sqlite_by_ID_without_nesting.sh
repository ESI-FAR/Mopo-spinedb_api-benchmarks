SETUP="
import json
import sqlite3
import timeit

def get_datapoint(DB_URL):
    with sqlite3.connect(DB_URL) as con:
        cur = con.cursor()
        cur.execute('SELECT value from parameter_value WHERE id=256351')
        table = cur.fetchall()

    #print(json.loads(table[0][0])['scen'][-1][-1])
    return json.loads(table[0][0])['scen'][-1][-1]
"

echo
echo "=== Benchmarking SQlite by ID without nesting. ==="
for db in \
  ../databases/BB_data_stripped_flat_list.sqlite \
  ../databases/ramdisk/BB_data_stripped_flat_list.sqlite \
  ; do
  echo
  echo "Using $db"
  python3 -m timeit -r 50 -s "$SETUP" "get_datapoint('$db')"
done
