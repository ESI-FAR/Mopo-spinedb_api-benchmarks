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

Benchmarking is done with the `timeit` package via the command line. Using it in this way produces faster times (and thus presumably more accurate) and produces more useful output (lowest runtime of a batch).

### Preparations

Create a `tmpfs` ramdisk at `databases/ramdisk/` and copy all necessary databases there:

```bash
 sudo mkdir databases/ramdisk
 sudo chmod 777 databases/ramdisk/
 sudo mount -t tmpfs -o size=1024m myramdisk databases/ramdisk
 cp databases/* databases/ramdisk/
```

This folder now lives in RAM instead of the hard drive. We will contrast database readings from both sources to evaluate the impact of I/O speeds.

### Databases

#### `BB_data.sqlite`
This is the full database. The four time series have different lengths, but the same data format.

- Size: 106 M
- Format:
    ```
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
            "data": [...]
          }
        ]
      ]
    }
    ```

#### `BB_data_stripped_list.sqlite`

Same as above, but all other `parameter_value`s are removed. The data is still a list.

- Size: 7.8 M
- Format: see above

#### `BB_data_stripped_flat_list.sqlite`

Removing the nesting.

- Size: 7.8 M
- Format:
    ```
    {
      "f00": [
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
      ],
      "avg": [...],
      "scen": [...],
      "median": [...]
    }
    ```

#### `BB_data_stripped_dict.sqlite`

The data is stored in lists of dictionaries, with keys "t" for time, and "v" for value, respectively.

- Size: 10 M
- Format:
    ```
    {
      "index_type": "str",
      "rank": 2,
      "data": [
        [
          "f00",
          {
            "type": "map",
            "index_type": "str",
            "rank": 1,
            "data": [
              {
                "t": "t000001",
                "v": 0.3199528015965129
              },
              {
                "t": "t000002",
                "v": 0.41037211746447516
              },
              ...,
              {
                "t": "t008735",
                "v": 0.030605335687853303
              },
              {
                "t": "t008736",
                "v": 0.0288792979152308
              }
            ]
          }
        ],
        [
          "avg",
          {
            "type": "map",
            "index_type": "str",
            "rank": 1,
            "data": [...]
          }
        ],
        [
          "scen",
          {
            "type": "map",
            "index_type": "str",
            "rank": 1,
            "data": [...]
          }
        ],
        [
          "median",
          {
            "type": "map",
            "index_type": "str",
            "rank": 1,
            "data": [...]
          }
        ]
      ]
    }

    ```

#### `BB_data_stripped_flat_dict.sqlite`

Removing the nesting, data is still a list of dictionaries.

- Size: 10 M
- Format:
    ```
    {
      "f00": [
        {
          "t": "t000001",
          "v": 0.3199528015965129
        },
        {
          "t": "t000002",
          "v": 0.41037211746447516
        },
        ...,
        {
          "t": "t008735",
          "v": 0.030605335687853303
        },
        {
          "t": "t008736",
          "v": 0.0288792979152308
        }
      ],
      "avg": [...],
      "scen": [...],
      "median": [...]
    }
    ```

#### `parquet.data`

Data is stored in a `pyarrow` table and saved in Parquet format.

- Size: 1.7 M
- Format:
  ```
  pa.Table(
    pa.ChunkedArray(
      pa.StructScalar(
        pa.MapScalar(  # "f00"
          tuple(
            pa.StringScalar,  # t000001
            pa.DoubleScalar   # 0.3199528015965129
          ),
          tuple(
            pa.StringScalar,  # t000001
            pa.DoubleScalar   # 0.41037211746447516
          ),
          ...
        ),
        pa.MapScalar(  # "avg"
          ...,
        ),
        pa.MapScalar(  # "scen"
          ...,
        ),
        pa.MapScalar(  # "median"
          ...,
        )
      )
    )
  )
  ```

### Benchmarking Results

Retrieving a single value from the `BB_data` database, the `parameter_value` of `entity_name='flow__node_wind__80NO'` and `id=256351`, from which we look at the _third time series_ and pick the _last_ item.


#### SpineDB_API by Entity Name

- File: `timeit_spinedb_api_by_entity_name.sh`
- Using:
  ```
  with DatabaseMapping('sqlite:///'+DB_URL) as db:
      item = db.get_items('parameter_value', entity_name='flow__node_wind__80NO')[0]

  return item['parsed_value'].values[2].values[-1]
  ```

##### SSD
- BB_data 265 ms
- BB_data_stripped_list 227 ms

##### Ramdisk
- BB_data 231 ms
- BB_data_stripped_list 222 ms

#### SpineDB_API by ID

- File: `timeit_spinedb_api_by_ID.sh`
- Using:
  ```
  with DatabaseMapping('sqlite:///'+DB_URL) as db:
      item = db.get_parameter_value_item(id=256351)

  return item['parsed_value'].values[2].values[-1]
  ```

##### SSD
- BB_data 336 ms
- BB_data_stripped_list 221 ms

##### Ramdisk
- BB_data 266 ms
- BB_data_stripped_list 215 ms

#### ADBC by ID

- File: `timeit_adbc.sh`
- Using:
  ```
  with adbc_driver_sqlite.dbapi.connect('file:'+DB_URL) as connection:
      with connection.cursor() as cur:
          cur.execute('SELECT value from parameter_value WHERE id=256351')
          table = cur.fetch_arrow_table()

  return json.loads(table['value'][0].as_py())['data'][2][1]['data'][-1][-1]
  ```

##### SSD
- BB_data 71.3 ms
- BB_data_stripped_list 66.4 ms

##### Ramdisk
- BB_data 62.8 ms
- BB_data_stripped_list 64.0 ms

#### ADBC queryable JSON list

- File: `timeit_adbc_JSON_query_list.sh`
- Using:
  ```
  with adbc_driver_sqlite.dbapi.connect('file:'+DB_URL) as connection:
      with connection.cursor() as cur:
          cur.execute('SELECT json_extract(parameter_value.value, \'$.scen[#-1][#-1]\') FROM parameter_value WHERE id=256351;')
          table = cur.fetch_arrow_table()

  return table[0][0].as_py()
  ```

##### SSD
- BB_data_stripped_flat_list 17.2 ms

##### Ramdisk
- BB_data_stripped_flat_list 13.7 ms

#### ADBC queryable JSON dict

- File: `timeit_adbc_JSON_query_dict.sh`
- Using:
  ```
  with adbc_driver_sqlite.dbapi.connect('file:'+DB_URL) as connection:
      with connection.cursor() as cur:
          cur.execute('SELECT json_extract(parameter_value.value, \'$.scen[#-1].v\') FROM parameter_value WHERE id=256351;')
          table = cur.fetch_arrow_table()

  return table[0][0].as_py()
  ```

##### SSD
- BB_data_stripped_flat_dict 23.5 ms

##### Ramdisk
- BB_data_stripped_flat_dict 18.7 ms

#### SQlite by ID

- File: `timeit_sqlite_by_ID.sh`
- Using:
  ```
  with sqlite3.connect(DB_URL) as con:
      cur = con.cursor()
      cur.execute('SELECT value from parameter_value WHERE id=256351')
      table = cur.fetchall()

  return json.loads(table[0][0])['data'][2][1]['data'][-1][-1]
  ```

##### SSD
- BB_data 67.2 ms
- BB_data_stripped_list 65.2 ms

##### Ramdisk
- BB_data 61.9 ms
- BB_data_stripped_list 61.5 ms

#### SQlite by ID, no nesting

- File: `timeit_sqlite_by_ID_without_nesting.sh`
- Using:
  ```
  with sqlite3.connect(DB_URL) as con:
      cur = con.cursor()
      cur.execute('SELECT value from parameter_value WHERE id=256351')
      table = cur.fetchall()

  return json.loads(table[0][0])['scen'][-1][-1]
  ```

##### SSD
- BB_data_stripped_flat_list 60.4 ms

##### Ramdisk
- BB_data_stripped_flat_list 55.7 ms

#### SQlite by ID, queryable JSON list

- File: `timeit_sqlite_by_ID_queryable_list.sh`
- Using:
  ```
  with sqlite3.connect(DB_URL) as con:
      cur = con.cursor()
      cur.execute('SELECT json_extract(parameter_value.value, \'$.scen[#-1][#-1]\') FROM parameter_value WHERE id=256351;')
      table = cur.fetchall()

  return table[0][0]
  ```

##### SSD
- BB_data_stripped_flat_list 12.3 ms

##### Ramdisk
- BB_data_stripped_flat_list 9.26 ms

#### SQlite by ID, queryable JSON dict

- File: `timeit_sqlite_by_ID_queryable_dict.sh`
- Using:
  ```
  with sqlite3.connect(DB_URL) as con:
      cur = con.cursor()
      cur.execute('SELECT json_extract(parameter_value.value, \'$.scen[#-1].v\') FROM parameter_value WHERE id=256351;')
      table = cur.fetchall()

  return table[0][0]
  ```

##### SSD
- BB_data_stripped_flat_dict 17.5 ms

##### Ramdisk
- BB_data_stripped_flat_dict 13.6 ms

#### Parquet

- File: `timeit_parquet.sh`
- Using:
  ```
  return pq.read_table(DB_URL)['data'][0]['scen'][-1][1]
  ```

##### SSD
- data.parquet 4.83 ms

##### Ramdisk
- data.parquet 4.91 ms
