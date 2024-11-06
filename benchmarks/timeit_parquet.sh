SETUP="
import pyarrow.parquet as pq
import timeit


def get_datapoint(DB_URL):
    #print(pq.read_table(DB_URL)['data'][0]['scen'][-1][1])
    return pq.read_table(DB_URL)['data'][0]['scen'][-1][1]
"

echo
echo "=== Benchmarking Parquet. ==="
for db in \
  ../databases/data.parquet \
  ../databases/ramdisk/data.parquet \
  ; do
  echo
  echo "Using $db"
  python3 -m timeit -r 50 -s "$SETUP" "get_datapoint('$db')"
done
