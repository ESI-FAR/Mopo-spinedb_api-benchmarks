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
