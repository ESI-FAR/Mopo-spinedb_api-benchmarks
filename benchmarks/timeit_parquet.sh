SETUP="
import pyarrow.parquet as pq
import timeit

DB_URL = '/tmp/ramdisk/data.parquet'

def get_datapoint(DB_URL):
    return pq.read_table(DB_URL)['data'][0][2][-1][1]
"

python3 -m timeit -r 50 -s "$SETUP" "get_datapoint(DB_URL)"
