# Testing Profilers

## Deterministic (event-based)

### `cProfile`
https://docs.python.org/3.12/library/profile.html

#### Visualization
- snakeviz
  https://github.com/jiffyclub/snakeviz
- tuna
  https://github.com/nschloe/tuna

### `yappi`
https://github.com/sumerc/yappi/tree/master

#### Visualization
- snakeviz
  https://github.com/jiffyclub/snakeviz
- tuna
  https://github.com/nschloe/tuna

## Sampling (statistical)
### `py-spy`
https://github.com/benfred/py-spy
- as of 2024-07-24 not compatible with Python 3.12 (yet)

### `scalene`
https://github.com/plasma-umass/scalene

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

## Omitted
### Linux Perf \w Python 3.12
Too complicated to set up:
- kernel-version-dependent `linux-tools-XXX` package
- compile Python with (leaf) frame pointers
