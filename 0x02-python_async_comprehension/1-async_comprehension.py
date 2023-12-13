#!/usr/bin/env python3

'''
    Async Comprehensions
'''
from typing import Generator, List

async_generator = __import__('0-async_generator').async_generator

async def async_comprehension() -> List[float]:
    '''
        Returns the 10 random numbers.
    '''
    return [i async for i in async_generator()]
