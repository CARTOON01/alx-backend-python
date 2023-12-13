#!/usr/bin/env python3

'''
    Task Zero
'''
from typing import Generator
import asyncio
import asyncio

async def async_generator() -> Generator[float, None, None]:
    '''
        Async Generator
    '''
    for i in range(10):
        await asyncio.sleep(1)
        yield random.random * 10