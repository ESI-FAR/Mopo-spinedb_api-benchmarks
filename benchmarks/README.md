# Performance Analyses for SpineDB_API Scenarios

Two types of performance analyses are performed: profiling and benchmarking. Profiling gives insight in _where_ time is spent during certain operations, but is often not too accurate on the exact amount of time spent. Benchmarking measures the overall time a script needs to execute without interfering during runtime. Benchmarking results are thus well comparable.

## Profiling

### Deterministic (Event-Based)

#### `cProfile`
https://docs.python.org/3.12/library/profile.html

`python -m cProfile -o profiles/FILENAME.pstats script.py script_args`

#### `yappi`
https://github.com/sumerc/yappi/tree/master

`yappi -o profiles/FILENAME.pstats script.py script_args`

### Sampling (Statistical)
#### `py-spy`
https://github.com/benfred/py-spy
- as of 2024-07-24 not compatible with Python 3.12 (yet)

#### `scalene`
https://github.com/plasma-umass/scalene

`scalene --cpu-sampling-rate 0.001 script.py script_args`

#### `pyinstrument`
https://github.com/joerick/pyinstrument

Visualizations in addition to the `pstats` visualizations:
- txt
- html
- speedscope
  https://github.com/jlfwong/speedscope
  https://www.speedscope.app/

`pyinstrument -o profiles/FILENAME.pstats -r pstats script.py script_args`

### Visualization
- snakeviz
  https://github.com/jiffyclub/snakeviz
  `snakeviz profiles/FILENAME.pstats`
- tuna
  https://github.com/nschloe/tuna
  `tuna profiles/FILENAME.pstats`
- pyprof2calltree/kcachegrind
  https://github.com/pwaller/pyprof2calltree/
  https://kcachegrind.sourceforge.net/html/Home.html
  `pyprof2calltree -i profiles/FILENAME.pstats -o profiles/FILENAME.calltree`
  `kcachegrind profiles/FILENAME.calltree`

### Omitted
#### Linux Perf \w Python 3.12
Too complicated to set up:
- kernel-version-dependent `linux-tools-XXX` package
- compile Python with (leaf) frame pointers

## Benchmarking

Benchmarking is done with the `timeit` package via the command line. Using it in this way is faster (and thus presumably more accurate) and produces more useful output (lowest runtime of a batch).

### Preparations

Create a `tmpfs` ramdisk at `databases/ramdisk/` and copy all necessary databases there:

```bash
 sudo mkdir databases/ramdisk
 sudo chmod 777 databases/ramdisk/
 sudo mount -t tmpfs -o size=1024m myramdisk databases/ramdisk
 cp databases/* databases/ramdisk/
```

### Databases

#### `BB_data.sqlite`
This is the full database. The four time series have different lengths, but the same data format.

- Size: 106M
- Format:```
{
  "index_type": "str",
  "data": [
    [
      "f00",
      {
        "type": "map",
        "index_type": "str",
        "data": [
          [
            "t000001",
            0.3199528015965129
          ],
          [
            "t000002",
            0.41037211746447516
          ],
	  ...,
          [
            "t008735",
            0.030605335687853303
          ],
          [
            "t008736",
            0.0288792979152308
          ]
        ]
      }
    ],
    [
      "avg",
      {
        "type": "map",
        "index_type": "str",
        "data": [...]
      }
    ],
    [
      "scen",
      {
        "type": "map",
        "index_type": "str",
        "data": [...]
      }
    ],
    [
      "median",
      {
        "type": "map",
        "index_type": "str",
        "data": []
      }
    ]
  ]
}
```

#### `BB_data_stripped.sqlite`

Same as above, but all other `parameter_value`s are removed.

- Size: 7.8M
- Format: see above

#### `BB_data_stripped_flat.sqlite`
TODO

### Benchmarking Results

Retrieving a single value from the `BB_data` database, the `parameter_value` of `entity_name='flow__node_wind__80NO'` and `id=256351`, from which we look at the _third time series_ and pick the _last_ item.


#### SpineDB_API by Entity Name

Using `get_items('parameter_value', entity_name='flow__node_wind__80NO')`.

##### SSD
BB_data 261ms
BB_data_stripped 227ms

##### Ramdisk
BB_data 226ms
BB_data_stripped 225ms

#### spinedb_api by ID

SSD
BB_data 333ms
BB_data_stripped 220ms

Ramdisk
BB_data 266ms
BB_data_stripped 219ms

#### ADBC by ID

SSD
BB_data 64.9 ms
BB_data_stripped 68.2 ms

Ramdisk
BB_data 64.0 ms
BB_data_stripped 63.0 ms

#### ADBC queryable JSON

SSD
BB_data 21.2 ms
BB_data_stripped 21.1 ms
BB_data_stripped_queryable 23.5 ms

Ramdisk
BB_data 18.0 ms
BB_data_stripped 17.7 ms
BB_data_stripped_queryable 18.9 ms

#### Parquet

SSD
data.parquet 4.94 ms

Ramdisk
data.parquet 4.92 ms

#### SQlite by ID, queryable JSON

SSD
BB_data_stripped_queryable 17.7 ms

Ramdisk
BB_data_stripped_queryable 13.6 ms

#### SQlite by ID, no nesting

SSD
BB_data_stripped_flat 58.6 ms

Ramdisk
BB_data_stripped_flat 56.2 ms

#### SQlite by ID

SSD
BB_data 67.2 ms
BB_data_stripped 66.5 ms

Ramdisk
BB_data 62.8 ms
BB_data_stripped 62.0 ms

