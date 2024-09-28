# `tqdmnd`: `tqdm` in Multiple Dimensions

`tqdmnd` is an N-dimensional wrapper of tqdm providing an iterator and
progress bar over the product of multiple iterators.

Example Usage:
```python
from tqdmnd import tqdmnd
for x, y in tqdmnd(5,6):
    pass
```
is equivalent to
```python
for x in range(5):
    for y in range(6):
        pass
```
but with a tqdm progress bar printed to standard output.
