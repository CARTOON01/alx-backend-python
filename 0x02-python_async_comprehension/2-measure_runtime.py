#!/usr/bin/env python3

'''
     Run time for four parallel comprehensions 
'''

import asyncio
import time
from importlib import import_module as using

async_comprehension = using('1-async_comprehension').async_comprehension

async def measure_runtime() -> float:
    '''
        Returns the total runtime for four parallel comprehensions.
    '''
    start = time.time()
    await asyncio.gather(*(async_comprehension() for i in range(4)))
    end = time.time()
    return end - start