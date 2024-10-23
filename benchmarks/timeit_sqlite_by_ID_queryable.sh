SETUP="
import json
import sqlite3
import timeit


def get_datapoint(DB_URL):
    with sqlite3.connect(DB_URL) as con:
        cur = con.cursor()
        item = cur.execute('SELECT json_extract(parameter_value.value, \'$.scen[#-1].v\') FROM parameter_value WHERE id=256351;')
        table = cur.fetchall()

    return table[0][0]
"

echo "Benchmarking SQlite by ID with queryable JSON."
for db in \
  ../databases/BB_data_stripped_queryable.sqlite \
  ../databases/ramdisk/BB_data_stripped_queryable.sqlite \
  ; do
  echo
  echo "Using $db"
  python3 -m timeit -r 50 -s "$SETUP" "get_datapoint('$db')"
done
