# BRIG
It is a repository for all modified functions and classes.

## Installation
```
pip install brig
```

## Usage
### PoolExecutor
It is a modified function of a Poolexecutor function in python to support 'tqdm' progress bar and showing error in thread. Below is the example code to import it,
```
import time
from brig.PoolExecutor import ThreadPool

def sleep(a, b, c, d):
    time.sleep(1) 

prog = tqdm.tqdm(total=300)
with ThreadPool(max_workers=20, progressor=prog) as pool:
    for i in range(300):
        pool.submit(sleep, 1, 2, 3, 4)
```
