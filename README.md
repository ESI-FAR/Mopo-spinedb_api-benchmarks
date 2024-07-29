# Testing Profilers

## Deterministic (event-based)

### `cProfile`
https://docs.python.org/3.12/library/profile.html

#### Visualization
- snakeviz
  https://github.com/jiffyclub/snakeviz
- tuna
  https://github.com/nschloe/tuna

#### Usage
`python -m cProfile -o profiles/FILENAME.pstats script.py script_args`

`tuna profiles/FILENAME.pstats`, or
`snakeviz profiles/FILENAME.pstats`

### `yappi`
https://github.com/sumerc/yappi/tree/master

#### Visualization
- snakeviz
  https://github.com/jiffyclub/snakeviz
- tuna
  https://github.com/nschloe/tuna

#### Usage
`yappi -o profiles/FILENAME.pstats script.py script_args`

`tuna profiles/FILENAME.pstats`, or
`snakeviz profiles/FILENAME.pstats`

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
- txt
- html
- speedscope
  https://github.com/jlfwong/speedscope
  https://www.speedscope.app/
- snakeviz
  https://github.com/jiffyclub/snakeviz
- tuna
  https://github.com/nschloe/tuna

#### Usage
`pyinstrument -o profiles/FILENAME.pstats -r pstats script.py script_args`

## Omitted
### Linux Perf \w Python 3.12
Too complicated to set up:
- kernel-version-dependent `linux-tools-XXX` package
- compile Python with (leaf) frame pointers
