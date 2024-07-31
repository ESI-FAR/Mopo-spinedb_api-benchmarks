# Testing Profilers

## Deterministic (event-based)

### `cProfile`
https://docs.python.org/3.12/library/profile.html

#### Usage
`python -m cProfile -o profiles/FILENAME.pstats script.py script_args`

### `yappi`
https://github.com/sumerc/yappi/tree/master

#### Usage
`yappi -o profiles/FILENAME.pstats script.py script_args`

## Sampling (statistical)
### `py-spy`
https://github.com/benfred/py-spy
- as of 2024-07-24 not compatible with Python 3.12 (yet)

### `scalene`
https://github.com/plasma-umass/scalene

#### Usage
`scalene --cpu-sampling-rate 0.001 script.py script_args`

### `pyinstrument`
https://github.com/joerick/pyinstrument

#### Visualization
(in addition to the `pstats` visualizations)
- txt
- html
- speedscope
  https://github.com/jlfwong/speedscope
  https://www.speedscope.app/

#### Usage
`pyinstrument -o profiles/FILENAME.pstats -r pstats script.py script_args`

## Visualization
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

## Omitted
### Linux Perf \w Python 3.12
Too complicated to set up:
- kernel-version-dependent `linux-tools-XXX` package
- compile Python with (leaf) frame pointers
